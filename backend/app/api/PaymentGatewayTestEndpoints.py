# PaymentGatewayTestEndpoints.py
# Test endpoints for payment gateway integration testing

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import aiohttp
from loguru import logger

router = APIRouter(
    prefix="/test/payment-gateway",
    tags=["Payment Gateway Testing"]
)


class PaymentMessage(BaseModel):
    """Payment message to send to the gateway"""
    kiosk_id: str = Field(..., description="Kiosk identifier", example="KIOSK_001")
    order_id: int = Field(..., description="Order ID", example=12345)
    sum: int = Field(..., description="Payment amount in kopecks", example=150000)


class CustomMessage(BaseModel):
    """Custom message to send to the gateway"""
    message: Dict[str, Any] = Field(..., description="Custom JSON message", example={
        "type": "test",
        "data": {
            "field1": "value1",
            "field2": 123
        }
    })


class MessageResponse(BaseModel):
    """Response from gateway"""
    success: bool
    status_code: int
    response_data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@router.post("/send-payment", response_model=MessageResponse, summary="Send payment message to gateway")
async def send_payment_message(payment: PaymentMessage):
    """
    Отправить JSON сообщение на оплату к платежному шлюзу по адресу web-production-a21a7.up.railway.app/send.

    Структура сообщения соответствует формату для эмулятора платежного терминала.
    """
    gateway_url = "https://web-production-a21a7.up.railway.app/send"

    payload = {
        "kiosk_id": payment.kiosk_id,
        "order_id": payment.order_id,
        "sum": payment.sum
    }

    logger.info(f"Sending payment message to {gateway_url}: {payload}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                gateway_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                status_code = response.status

                try:
                    response_data = await response.json()
                except:
                    response_text = await response.text()
                    response_data = {"raw_response": response_text}

                logger.info(f"Gateway response: status={status_code}, data={response_data}")

                return MessageResponse(
                    success=status_code == 200,
                    status_code=status_code,
                    response_data=response_data
                )

    except aiohttp.ClientTimeout:
        logger.error("Request to gateway timed out")
        return MessageResponse(
            success=False,
            status_code=408,
            error="Request timeout"
        )

    except Exception as e:
        logger.error(f"Error sending message to gateway: {str(e)}")
        return MessageResponse(
            success=False,
            status_code=500,
            error=str(e)
        )


@router.post("/send-custom", response_model=MessageResponse, summary="Send custom message to gateway")
async def send_custom_message(custom: CustomMessage):
    """
    Отправить кастомное JSON сообщение к платежному шлюзу по адресу web-production-a21a7.up.railway.app/send.

    Позволяет отправить произвольную JSON структуру для тестирования различных сценариев.
    """
    gateway_url = "https://web-production-a21a7.up.railway.app/send"

    logger.info(f"Sending custom message to {gateway_url}: {custom.message}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                gateway_url,
                json=custom.message,
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                status_code = response.status

                try:
                    response_data = await response.json()
                except:
                    response_text = await response.text()
                    response_data = {"raw_response": response_text}

                logger.info(f"Gateway response: status={status_code}, data={response_data}")

                return MessageResponse(
                    success=status_code == 200,
                    status_code=status_code,
                    response_data=response_data
                )

    except aiohttp.ClientTimeout:
        logger.error("Request to gateway timed out")
        return MessageResponse(
            success=False,
            status_code=408,
            error="Request timeout"
        )

    except Exception as e:
        logger.error(f"Error sending custom message to gateway: {str(e)}")
        return MessageResponse(
            success=False,
            status_code=500,
            error=str(e)
        )


@router.get("/gateway-health", summary="Check gateway availability")
async def check_gateway_health():
    """
    Проверить доступность платежного шлюза.
    """
    gateway_url = "https://web-production-a21a7.up.railway.app/send"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                gateway_url,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                return {
                    "gateway_url": gateway_url,
                    "status": "available",
                    "status_code": response.status
                }

    except Exception as e:
        return {
            "gateway_url": gateway_url,
            "status": "unavailable",
            "error": str(e)
        }

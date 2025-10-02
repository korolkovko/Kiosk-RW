# payment_gateway.py
# Payment gateway integration with mockup functionality for testing

import asyncio
import uuid
import aiohttp
from typing import Dict, Any, Optional
from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class PaymentResult(str, Enum):
    """Payment processing results"""
    SUCCESS = "SUCCESS"
    DECLINED = "DECLINED"
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"


@dataclass
class PaymentRequest:
    """Payment request structure matching web emulator API"""
    kiosk_id: str
    order_id: int
    sum: int  # Amount in kopecks (integer)


@dataclass
class PaymentResponse:
    """Payment response structure matching web emulator API"""
    payment_id: int
    order_id: int
    session_id: str
    status: str  # SUCCESS|DECLINED|ERROR
    auth_code: Optional[str] = None
    rrn: Optional[str] = None
    transaction_id: str = "0"
    terminal_id: str = ""
    merchant_id: str = ""
    response_code: str = ""
    response_message: str = ""
    amount: int = 0  # Amount in kopecks
    currency_code: str = "643"
    payment_date: str = ""  # ISO datetime string
    completed_at: str = ""  # ISO datetime string
    receipt_available: bool = False
    field_90_raw: Optional[str] = None  # XML response from terminal
    customer_receipt: Optional[str] = None
    merchant_receipt: Optional[str] = None
    
    def __post_init__(self):
        if not self.payment_date:
            self.payment_date = datetime.utcnow().isoformat()
        if not self.completed_at:
            self.completed_at = datetime.utcnow().isoformat()


class PaymentGatewayConfig:
    """Configuration for payment gateway integration"""
    
    def __init__(self):
        # Load from centralized config
        from .integrations_config import get_integrations_config
        config = get_integrations_config().payment
        
        # Copy settings from centralized config
        self.mockup_mode = config.mockup_mode
        self.gateway_url = config.gateway_url
        self.merchant_id = config.merchant_id
        self.terminal_id = config.terminal_id
        self.api_key = config.api_key
        self.timeout_seconds = config.timeout_seconds
        self.use_ssl = config.use_ssl
        self.max_retries = config.max_retries
        
        # Mockup-specific settings (keep for backward compatibility)
        self.mockup_success_rate = 0.7  # 70% success rate for testing
        self.mockup_processing_delay = 1.5  # seconds


class PaymentGateway:
    """
    Payment gateway integration service.
    Currently implements mockup functionality for testing.
    """
    
    def __init__(self, config: PaymentGatewayConfig):
        self.config = config
        self._request_counter = 0
    
    async def process_payment(self, request: PaymentRequest) -> PaymentResponse:
        """
        Process payment request.
        In mockup mode, simulates payment processing with configurable success rate.
        """
        if self.config.mockup_mode:
            return await self._mockup_payment_processing(request)
        else:
            return await self._real_payment_processing(request)
    
    async def _mockup_payment_processing(self, request: PaymentRequest) -> PaymentResponse:
        """Mockup payment processing for testing."""
        # Simulate processing delay
        await asyncio.sleep(self.config.mockup_processing_delay)
        
        self._request_counter += 1
        
        # Simulate success/failure based on configured rate
        import random
        is_success = random.random() < self.config.mockup_success_rate
        
        if is_success:
            transaction_id = f"TXN_{uuid.uuid4().hex[:8].upper()}"
            return PaymentResponse(
                payment_id=self._request_counter,
                order_id=request.order_id,
                session_id=f"SES_{request.order_id}_{self._request_counter}",
                status="SUCCESS",
                auth_code=f"{self._request_counter:06d}",
                rrn=f"000010{self._request_counter:06d}",
                transaction_id=transaction_id,
                terminal_id="00092240",
                merchant_id="ZERO_CULTURE_MERCHANT",
                response_code="00",
                response_message="Approved",
                amount=request.sum,
                currency_code="643",
                customer_receipt=self._generate_mockup_customer_receipt(request),
                merchant_receipt=self._generate_mockup_merchant_receipt(request)
            )
        else:
            # Simulate different failure types
            failure_types = [
                ("05", "Do not honor", PaymentResult.DECLINED),
                ("51", "Insufficient funds", PaymentResult.DECLINED),
                ("91", "Issuer or switch inoperative", PaymentResult.ERROR),
                ("96", "System malfunction", PaymentResult.ERROR),
                ("TIMEOUT", "Request timeout", PaymentResult.TIMEOUT)
            ]
            
            code, message, result = random.choice(failure_types)
            
            return PaymentResponse(
                payment_id=0,
                order_id=request.order_id,
                session_id=f"SES_{request.order_id}_FAILED",
                status=result.value,
                response_code=code,
                response_message=message,
                amount=request.sum
            )
    
    async def _real_payment_processing(self, request: PaymentRequest) -> PaymentResponse:
        """
        Real payment processing integration with web emulator.
        Calls the actual payment gateway/emulator via HTTP.
        """
        import json
        from .integrations_config import get_integrations_config
        
        config = get_integrations_config().payment
        
        if not config.gateway_url:
            raise Exception("Payment gateway URL not configured")
        
        # Prepare request payload matching web emulator format
        payload = {
            "kiosk_id": request.kiosk_id,
            "order_id": request.order_id,
            "sum": request.sum
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if config.api_key:
            headers["Authorization"] = f"Bearer {config.api_key}"
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=config.timeout_seconds)) as session:
                async with session.post(
                    f"{config.gateway_url}/mocks/payment",
                    json=payload,
                    headers=headers,
                    ssl=config.use_ssl
                ) as response:
                    
                    if response.status == 200:
                        # Parse successful response
                        response_data = await response.json()
                        
                        # Map web emulator response to our PaymentResponse format
                        return PaymentResponse(
                            payment_id=response_data["payment_id"],
                            order_id=response_data["order_id"],
                            session_id=response_data["session_id"],
                            status=response_data["status"],
                            auth_code=response_data.get("auth_code"),
                            rrn=response_data.get("rrn"),
                            transaction_id=response_data.get("transaction_id", "0"),
                            terminal_id=response_data.get("terminal_id", ""),
                            merchant_id=response_data.get("merchant_id", ""),
                            response_code=response_data.get("response_code", ""),
                            response_message=response_data.get("response_message", ""),
                            amount=response_data.get("amount", 0),
                            currency_code=response_data.get("currency_code", "643"),
                            payment_date=response_data.get("payment_date", ""),
                            completed_at=response_data.get("completed_at", ""),
                            receipt_available=response_data.get("receipt_available", False),
                            field_90_raw=response_data.get("field_90_raw"),
                            customer_receipt=response_data.get("customer_receipt"),
                            merchant_receipt=response_data.get("merchant_receipt")
                        )
                    
                    elif response.status == 503:
                        # Service unavailable
                        return PaymentResponse(
                            payment_id=0,
                            order_id=request.order_id,
                            session_id=f"{request.order_id}-unavailable",
                            status="ERROR",
                            response_code="503",
                            response_message="Service Unavailable",
                            amount=request.sum
                        )
                    
                    elif response.status == 500:
                        # Internal server error
                        return PaymentResponse(
                            payment_id=0,
                            order_id=request.order_id,
                            session_id=f"{request.order_id}-error",
                            status="ERROR",
                            response_code="500",
                            response_message="Internal Server Error",
                            amount=request.sum
                        )
                    
                    else:
                        # Other HTTP errors
                        error_detail = await response.text()
                        return PaymentResponse(
                            payment_id=0,
                            order_id=request.order_id,
                            session_id=f"{request.order_id}-http-error",
                            status="ERROR",
                            response_code=str(response.status),
                            response_message=f"HTTP {response.status}: {error_detail}",
                            amount=request.sum
                        )
        
        except aiohttp.ClientTimeout:
            return PaymentResponse(
                payment_id=0,
                order_id=request.order_id,
                session_id=f"{request.order_id}-timeout",
                status="TIMEOUT",
                response_code="TIMEOUT",
                response_message="Payment gateway timeout",
                amount=request.sum
            )
        
        except Exception as e:
            return PaymentResponse(
                payment_id=0,
                order_id=request.order_id,
                session_id=f"{request.order_id}-exception",
                status="ERROR",
                response_code="ERROR",
                response_message=f"Payment processing error: {str(e)}",
                amount=request.sum
            )
    
    def _generate_mockup_customer_receipt(self, request: PaymentRequest) -> str:
        """Generate mockup customer receipt."""
        return f"""
CUSTOMER RECEIPT
================
Order: {request.order_id}
Amount: {request.sum/100:.2f} RUB
Kiosk: {request.kiosk_id}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
================
Thank you for your purchase!
        """.strip()
    
    def _generate_mockup_merchant_receipt(self, request: PaymentRequest) -> str:
        """Generate mockup merchant receipt."""
        return f"""
MERCHANT RECEIPT
================
Order: {request.order_id}
Amount: {request.sum/100:.2f} RUB
Terminal: MOCKUP_TERMINAL
Kiosk: {request.kiosk_id}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
================
        """.strip()


# Global payment gateway instance
_payment_gateway: Optional[PaymentGateway] = None


def get_payment_gateway() -> PaymentGateway:
    """Get or create payment gateway instance."""
    global _payment_gateway
    if _payment_gateway is None:
        config = PaymentGatewayConfig()
        _payment_gateway = PaymentGateway(config)
    return _payment_gateway


def configure_payment_gateway(config: PaymentGatewayConfig) -> None:
    """Configure payment gateway with custom settings."""
    global _payment_gateway
    _payment_gateway = PaymentGateway(config)
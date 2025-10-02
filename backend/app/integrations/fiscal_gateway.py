# fiscal_gateway.py
# Fiscal gateway integration with mockup functionality for KKT/fiscal printer testing

import asyncio
import uuid
import aiohttp
from typing import Dict, Any, Optional, List
from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class FiscalResult(str, Enum):
    """Fiscal processing results"""
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"


@dataclass
class FiscalItem:
    """Fiscal item structure matching web emulator API"""
    item_id: int
    item_description: str
    item_price_net: int  # In kopecks
    item_price_gross: int  # In kopecks
    item_vat_value: int  # In kopecks
    quantity: int


@dataclass
class FiscalRequest:
    """Fiscal request structure matching web emulator API"""
    order_id: int
    kiosk_id: str
    items: List[FiscalItem]
    total_net: int  # In kopecks
    total_vat: int  # In kopecks
    total_gross: int  # In kopecks
    payment_method: str = "CARD"


@dataclass
class FiscalReceiptItem:
    """Fiscal receipt item structure from web emulator response"""
    item_id: int
    description: str
    quantity: int
    price_net: int  # In kopecks
    vat: int  # In kopecks
    price_gross: int  # In kopecks


@dataclass
class FiscalReceiptData:
    """Fiscal receipt data structure from web emulator response"""
    ofd_reg_number: str
    fiscal_document_number: str
    fn_number: str
    order_id: int
    issued_at: str  # ISO datetime string
    items: List[FiscalReceiptItem]
    total_net: int  # In kopecks
    total_vat: int  # In kopecks
    total_gross: int  # In kopecks
    message: str


@dataclass
class FiscalResponse:
    """Fiscal response structure matching web emulator API"""
    status: str  # OK|NOT_OK
    fiscal_receipt: Optional[FiscalReceiptData] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    processed_at: datetime = None
    
    def __post_init__(self):
        if self.processed_at is None:
            self.processed_at = datetime.utcnow()


class FiscalGatewayConfig:
    """Configuration for fiscal gateway integration"""

    def __init__(self):
        # Load from centralized config
        from .integrations_config import get_integrations_config
        config = get_integrations_config().fiscal

        # Copy settings from centralized config
        self.mockup_mode = config.mockup_mode
        self.kkt_host = config.kkt_host
        self.kkt_port = config.kkt_port
        self.kkt_timeout = config.timeout_seconds
        self.fiscal_number = config.fiscal_number
        self.inn = config.inn
        self.ofd_provider = config.ofd_provider
        self.fiscal_mode = config.fiscal_mode
        self.use_ssl = config.use_ssl
        self.max_retries = config.max_retries
        self.timeout_seconds = config.timeout_seconds

        # Mockup-specific settings (keep for backward compatibility)
        self.mockup_success_rate = 0.9  # 90% success rate for fiscal operations
        self.mockup_processing_delay = 0.8  # seconds
        self.tax_system = 1  # Tax system code


class FiscalGateway:
    """
    Fiscal gateway integration service.
    Currently implements mockup functionality for KKT/fiscal printer testing.
    """
    
    def __init__(self, config: FiscalGatewayConfig):
        self.config = config
        self._document_counter = 1000  # Starting fiscal document number
    
    async def process_fiscalization(self, request: FiscalRequest) -> FiscalResponse:
        """
        Process fiscal document creation.
        In mockup mode, simulates KKT fiscal processing.
        """
        if self.config.mockup_mode:
            return await self._mockup_fiscal_processing(request)
        else:
            return await self._real_fiscal_processing(request)
    
    async def _mockup_fiscal_processing(self, request: FiscalRequest) -> FiscalResponse:
        """Mockup fiscal processing for testing."""
        # Simulate processing delay
        await asyncio.sleep(self.config.mockup_processing_delay)
        
        self._document_counter += 1
        
        # Simulate success/failure based on configured rate
        import random
        is_success = random.random() < self.config.mockup_success_rate
        
        if is_success:
            fiscal_doc_number = f"FD{self._document_counter:06d}"
            receipt_number = f"RCP{self._document_counter:06d}"
            
            # Create fiscal receipt data
            receipt_items = [
                FiscalReceiptItem(
                    item_id=item.item_id,
                    description=item.item_description,
                    quantity=item.quantity,
                    price_net=item.item_price_net,
                    vat=item.item_vat_value,
                    price_gross=item.item_price_gross
                )
                for item in request.items
            ]
            
            receipt_data = FiscalReceiptData(
                ofd_reg_number="1234567890123456",
                fiscal_document_number=fiscal_doc_number,
                fn_number="9999078900004312",
                order_id=request.order_id,
                issued_at=datetime.utcnow().isoformat(),
                items=receipt_items,
                total_net=request.total_net,
                total_vat=request.total_vat,
                total_gross=request.total_gross,
                message="Fiscal document created successfully"
            )
            
            return FiscalResponse(
                status="OK",
                fiscal_receipt=receipt_data
            )
        else:
            # Simulate different failure types
            failure_types = [
                ("01", "Fiscal storage error", FiscalResult.ERROR),
                ("02", "OFD connection failed", FiscalResult.ERROR),
                ("03", "Invalid fiscal data", FiscalResult.FAILED),
                ("TIMEOUT", "KKT timeout", FiscalResult.TIMEOUT)
            ]
            
            code, message, result = random.choice(failure_types)
            
            return FiscalResponse(
                status="NOT_OK",
                error_code=code,
                error_message=message
            )
    
    async def _real_fiscal_processing(self, request: FiscalRequest) -> FiscalResponse:
        """
        Real fiscal processing integration with web emulator.
        Calls the actual fiscal gateway/emulator via HTTP.
        """
        import json
        from .integrations_config import get_integrations_config
        
        config = get_integrations_config().fiscal
        
        if not config.kkt_host:
            raise Exception("Fiscal gateway URL not configured")
        
        # Prepare request payload matching web emulator format
        payload = {
            "order_id": request.order_id,
            "kiosk_id": request.kiosk_id,
            "items": [
                {
                    "item_id": item.item_id,
                    "item_description": item.item_description,
                    "item_price_net": item.item_price_net,
                    "item_price_gross": item.item_price_gross,
                    "item_vat_value": item.item_vat_value,
                    "quantity": item.quantity
                }
                for item in request.items
            ],
            "total_net": request.total_net,
            "total_vat": request.total_vat,
            "total_gross": request.total_gross,
            "payment_method": request.payment_method
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=config.timeout_seconds)) as session:
                async with session.post(
                    f"{config.kkt_host}/mocks/fiscal",
                    json=payload,
                    headers=headers,
                    ssl=config.use_ssl
                ) as response:
                    
                    if response.status == 200:
                        # Parse response
                        response_data = await response.json()
                        
                        if response_data.get("status") == "OK":
                            # Success response
                            fiscal_receipt = response_data["fiscal_receipt"]
                            receipt_items = [
                                FiscalReceiptItem(
                                    item_id=item["item_id"],
                                    description=item["description"],
                                    quantity=item["quantity"],
                                    price_net=item["price_net"],
                                    vat=item["vat"],
                                    price_gross=item["price_gross"]
                                )
                                for item in fiscal_receipt["items"]
                            ]
                            
                            receipt_data = FiscalReceiptData(
                                ofd_reg_number=fiscal_receipt["ofd_reg_number"],
                                fiscal_document_number=fiscal_receipt["fiscal_document_number"],
                                fn_number=fiscal_receipt["fn_number"],
                                order_id=fiscal_receipt["order_id"],
                                issued_at=fiscal_receipt["issued_at"],
                                items=receipt_items,
                                total_net=fiscal_receipt["total_net"],
                                total_vat=fiscal_receipt["total_vat"],
                                total_gross=fiscal_receipt["total_gross"],
                                message=fiscal_receipt["message"]
                            )
                            
                            return FiscalResponse(
                                status="OK",
                                fiscal_receipt=receipt_data
                            )
                        else:
                            # Failure response
                            return FiscalResponse(
                                status="NOT_OK",
                                error_code=response_data.get("error_code", "UNKNOWN"),
                                error_message=response_data.get("error_message", "Fiscal processing failed")
                            )
                    
                    elif response.status == 503:
                        return FiscalResponse(
                            status="NOT_OK",
                            error_code="SERVICE_UNAVAILABLE",
                            error_message="Fiscal service unavailable"
                        )
                    
                    elif response.status == 500:
                        return FiscalResponse(
                            status="NOT_OK",
                            error_code="INTERNAL_ERROR",
                            error_message="Fiscal service internal error"
                        )
                    
                    else:
                        error_detail = await response.text()
                        return FiscalResponse(
                            status="NOT_OK",
                            error_code=f"HTTP_{response.status}",
                            error_message=f"HTTP {response.status}: {error_detail}"
                        )
        
        except aiohttp.ClientTimeout:
            return FiscalResponse(
                status="NOT_OK",
                error_code="TIMEOUT",
                error_message="Fiscal gateway timeout"
            )
        
        except Exception as e:
            return FiscalResponse(
                status="NOT_OK",
                error_code="ERROR",
                error_message=f"Fiscal processing error: {str(e)}"
            )
    
    def _generate_mockup_fiscal_receipt(self, request: FiscalRequest, doc_number: str) -> Dict[str, Any]:
        """Generate mockup fiscal receipt structure."""
        return {
            "fiscal_document_number": doc_number,
            "fiscal_receipt_number": f"RCP{doc_number[2:]}",
            "inn": self.config.inn,
            "fiscal_mode": self.config.fiscal_mode,
            "order_id": request.order_id,
            "total_gross": request.total_gross,
            "payment_method": request.payment_method,
            "created_at": datetime.utcnow().isoformat(),
            "ofd_status": "sent",
            "mockup": True
        }
    
    async def check_fiscal_status(self, operation_id: str) -> Optional[FiscalResponse]:
        """
        Check status of fiscal operation.
        Used for polling-based integrations.
        """
        if self.config.mockup_mode:
            # In mockup mode, assume immediate processing
            return None
        else:
            # TODO: Implement real status checking
            raise NotImplementedError("Real fiscal status checking not implemented yet")


# Global fiscal gateway instance
_fiscal_gateway: Optional[FiscalGateway] = None


def get_fiscal_gateway() -> FiscalGateway:
    """Get or create fiscal gateway instance."""
    global _fiscal_gateway
    if _fiscal_gateway is None:
        config = FiscalGatewayConfig()
        _fiscal_gateway = FiscalGateway(config)
    return _fiscal_gateway


def configure_fiscal_gateway(config: FiscalGatewayConfig) -> None:
    """Configure fiscal gateway with custom settings."""
    global _fiscal_gateway
    _fiscal_gateway = FiscalGateway(config)
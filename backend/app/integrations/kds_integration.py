# kds_integration.py
# Kitchen Display System integration with mockup functionality for testing

import asyncio
import uuid
import aiohttp
from typing import Dict, Any, Optional, List
from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class KDSResult(str, Enum):
    """KDS processing results"""
    CONFIRMED = "CONFIRMED"
    ERROR = "ERROR"
    NO_RESPONSE = "NO_RESPONSE"
    TIMEOUT = "TIMEOUT"


class OrderPriority(str, Enum):
    """Order priority levels for kitchen"""
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"


@dataclass
class KDSOrderItem:
    """Order item structure for KDS matching web emulator API"""
    item_id: int
    description: str
    quantity: int


@dataclass
class KDSRequest:
    """KDS request structure matching web emulator API"""
    order_id: int
    kiosk_id: str
    items: List[KDSOrderItem]


@dataclass
class KDSResponse:
    """KDS response structure matching web emulator API"""
    status: str  # OK|NOT_OK
    kds_ticket_id: Optional[str] = None
    received_at: Optional[str] = None  # ISO datetime string
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    processed_at: datetime = None
    
    def __post_init__(self):
        if self.processed_at is None:
            self.processed_at = datetime.utcnow()


class KDSGatewayConfig:
    """Configuration for KDS integration"""

    def __init__(self):
        # Load from centralized config
        from .integrations_config import get_integrations_config
        config = get_integrations_config().kds

        # Copy settings from centralized config
        self.mockup_mode = config.mockup_mode
        self.kds_api_url = config.kds_api_url
        self.kds_api_key = config.kds_api_key
        self.kds_timeout = config.timeout_seconds
        self.kitchen_station_id = config.kitchen_station_id
        self.auto_confirm_orders = config.auto_confirm_orders
        self.use_ssl = config.use_ssl
        self.max_retries = config.max_retries
        self.timeout_seconds = config.timeout_seconds

        # Mockup-specific settings (keep for backward compatibility)
        self.mockup_success_rate = 0.95  # 95% success rate for KDS
        self.mockup_processing_delay = 0.5  # seconds
        self.mockup_prep_time_minutes = 15  # Default preparation time
        self.default_prep_time = 15  # minutes
        self.priority_prep_time_multiplier = 0.8  # High priority orders get 20% less time


class KDSGateway:
    """
    Kitchen Display System integration service.
    Currently implements mockup functionality for testing.
    """
    
    def __init__(self, config: KDSGatewayConfig):
        self.config = config
        self._order_counter = 1
    
    async def send_order_to_kitchen(self, request: KDSRequest) -> KDSResponse:
        """
        Send order to kitchen display system.
        In mockup mode, simulates kitchen order processing.
        """
        if self.config.mockup_mode:
            return await self._mockup_kds_processing(request)
        else:
            return await self._real_kds_processing(request)
    
    async def _mockup_kds_processing(self, request: KDSRequest) -> KDSResponse:
        """Mockup KDS processing for testing."""
        # Simulate processing delay
        await asyncio.sleep(self.config.mockup_processing_delay)
        
        self._order_counter += 1
        
        # Simulate success/failure based on configured rate
        import random
        is_success = random.random() < self.config.mockup_success_rate
        
        if is_success:
            # Calculate estimated completion time
            prep_time = self.config.mockup_prep_time_minutes
            if request.priority in [OrderPriority.HIGH, OrderPriority.URGENT]:
                prep_time = int(prep_time * self.config.priority_prep_time_multiplier)
            
            estimated_completion = datetime.utcnow().replace(
                minute=datetime.utcnow().minute + prep_time
            )
            
            return KDSResponse(
                operation_id=request.operation_id,
                result=KDSResult.CONFIRMED,
                kds_order_id=f"KDS{self._order_counter:04d}",
                estimated_completion_time=estimated_completion,
                response_code="00",
                response_message="Order accepted by kitchen",
                kitchen_notes=f"Prep time: {prep_time} min",
                raw_response=f"<kds_response>CONFIRMED:KDS{self._order_counter:04d}</kds_response>"
            )
        else:
            # Simulate different failure types
            failure_types = [
                ("01", "Kitchen system offline", KDSResult.ERROR),
                ("02", "Invalid order data", KDSResult.ERROR),
                ("TIMEOUT", "Kitchen system timeout", KDSResult.TIMEOUT),
                ("NO_RESP", "No response from kitchen", KDSResult.NO_RESPONSE)
            ]
            
            code, message, result = random.choice(failure_types)
            
            return KDSResponse(
                operation_id=request.operation_id,
                result=result,
                response_code=code,
                response_message=message,
                raw_response=f"<kds_response>FAILED:{code}</kds_response>"
            )
    
    async def _real_kds_processing(self, request: KDSRequest) -> KDSResponse:
        """
        Real KDS processing integration with web emulator.
        Calls the actual kitchen system/emulator via HTTP.
        """
        import json
        from .integrations_config import get_integrations_config
        
        config = get_integrations_config().kds
        
        if not config.kds_api_url:
            raise Exception("KDS API URL not configured")
        
        # Prepare request payload matching web emulator format
        payload = {
            "order_id": request.order_id,
            "kiosk_id": request.kiosk_id,
            "items": [
                {
                    "item_id": item.item_id,
                    "description": item.description,
                    "quantity": item.quantity
                }
                for item in request.items
            ]
        }
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if config.kds_api_key:
            headers["Authorization"] = f"Bearer {config.kds_api_key}"
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=config.timeout_seconds)) as session:
                async with session.post(
                    f"{config.kds_api_url}/mocks/kds",
                    json=payload,
                    headers=headers,
                    ssl=config.use_ssl
                ) as response:
                    
                    if response.status == 200:
                        # Parse response
                        response_data = await response.json()
                        
                        if response_data.get("status") == "OK":
                            # Success response
                            return KDSResponse(
                                status="OK",
                                kds_ticket_id=response_data.get("kds_ticket_id"),
                                received_at=response_data.get("received_at")
                            )
                        else:
                            # Failure response
                            return KDSResponse(
                                status="NOT_OK",
                                error_code=response_data.get("error_code", "UNKNOWN"),
                                error_message=response_data.get("error_message", "KDS processing failed")
                            )
                    
                    elif response.status == 503:
                        return KDSResponse(
                            status="NOT_OK",
                            error_code="SERVICE_UNAVAILABLE",
                            error_message="KDS service unavailable"
                        )
                    
                    elif response.status == 500:
                        return KDSResponse(
                            status="NOT_OK",
                            error_code="INTERNAL_ERROR",
                            error_message="KDS service internal error"
                        )
                    
                    else:
                        error_detail = await response.text()
                        return KDSResponse(
                            status="NOT_OK",
                            error_code=f"HTTP_{response.status}",
                            error_message=f"HTTP {response.status}: {error_detail}"
                        )
        
        except aiohttp.ClientTimeout:
            return KDSResponse(
                status="NOT_OK",
                error_code="TIMEOUT",
                error_message="KDS gateway timeout"
            )
        
        except Exception as e:
            return KDSResponse(
                status="NOT_OK",
                error_code="ERROR",
                error_message=f"KDS processing error: {str(e)}"
            )
    
    async def check_order_status(self, kds_order_id: str) -> Optional[Dict[str, Any]]:
        """
        Check order status in kitchen system.
        Used for polling order completion status.
        """
        if self.config.mockup_mode:
            # In mockup mode, simulate random completion
            import random
            if random.random() < 0.1:  # 10% chance order is ready
                return {
                    "kds_order_id": kds_order_id,
                    "status": "READY",
                    "completed_at": datetime.utcnow().isoformat(),
                    "notes": "Order ready for pickup"
                }
            return None
        else:
            # TODO: Implement real status checking
            raise NotImplementedError("Real KDS status checking not implemented yet")


# Global KDS gateway instance
_kds_gateway: Optional[KDSGateway] = None


def get_kds_gateway() -> KDSGateway:
    """Get or create KDS gateway instance."""
    global _kds_gateway
    if _kds_gateway is None:
        config = KDSGatewayConfig()
        _kds_gateway = KDSGateway(config)
    return _kds_gateway


def configure_kds_gateway(config: KDSGatewayConfig) -> None:
    """Configure KDS gateway with custom settings."""
    global _kds_gateway
    _kds_gateway = KDSGateway(config)
# printer_gateway.py
# Printer gateway integration with file-based printing for testing
# Prints realistic POS terminal receipts to /receipts folder

import asyncio
import os
from typing import Optional, Dict, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum


class PrinterResult(str, Enum):
    """Printer processing results"""
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"


@dataclass
class PrinterRequest:
    """Printer request structure for receipt printing"""
    order_id: int
    kiosk_id: str
    payment_data: Dict[str, Any]  # Payment response data for receipt
    receipt_type: str = "CUSTOMER"  # CUSTOMER or MERCHANT


@dataclass
class PrinterResponse:
    """Printer response structure"""
    status: str  # SUCCESS|FAILED|ERROR
    receipt_file_path: Optional[str] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    printed_at: datetime = None
    
    def __post_init__(self):
        if self.printed_at is None:
            self.printed_at = datetime.utcnow()


class PrinterGatewayConfig:
    """Configuration for printer gateway integration"""
    
    def __init__(self):
        # File-based printing configuration
        self.mockup_mode = True
        self.receipts_folder = "receipts"  # Relative to project root
        self.mockup_success_rate = 0.95  # 95% success rate for printing
        self.mockup_processing_delay = 0.5  # seconds
        
        # Real printer integration configuration (for future use)
        self.printer_host = ""
        self.printer_port = 0
        self.printer_timeout = 10
        self.printer_model = ""


class PrinterGateway:
    """
    Printer gateway integration service.
    Currently implements file-based printing for testing.
    """
    
    def __init__(self, config: PrinterGatewayConfig):
        self.config = config
        self._receipt_counter = 1
        
        # Ensure receipts folder exists
        os.makedirs(self.config.receipts_folder, exist_ok=True)
    
    async def print_receipt(self, request: PrinterRequest) -> PrinterResponse:
        """
        Print receipt to file.
        In mockup mode, saves receipt as text file to receipts folder.
        """
        if self.config.mockup_mode:
            return await self._mockup_receipt_printing(request)
        else:
            return await self._real_receipt_printing(request)
    
    async def _mockup_receipt_printing(self, request: PrinterRequest) -> PrinterResponse:
        """Mockup receipt printing for testing."""
        # Simulate processing delay
        await asyncio.sleep(self.config.mockup_processing_delay)
        
        self._receipt_counter += 1
        
        # Simulate success/failure based on configured rate
        import random
        is_success = random.random() < self.config.mockup_success_rate
        
        if is_success:
            # Generate receipt content
            receipt_content = self._generate_pos_terminal_receipt(request)
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"receipt_order_{request.order_id}_{timestamp}.txt"
            file_path = os.path.join(self.config.receipts_folder, filename)
            
            # Write receipt to file
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(receipt_content)
                
                return PrinterResponse(
                    status="SUCCESS",
                    receipt_file_path=file_path
                )
            except Exception as e:
                return PrinterResponse(
                    status="ERROR",
                    error_code="FILE_WRITE_ERROR",
                    error_message=f"Failed to write receipt file: {str(e)}"
                )
        else:
            # Simulate different failure types
            failure_types = [
                ("PAPER_JAM", "Printer paper jam", PrinterResult.FAILED),
                ("OUT_OF_PAPER", "Printer out of paper", PrinterResult.FAILED),
                ("PRINTER_OFFLINE", "Printer offline", PrinterResult.ERROR),
                ("TIMEOUT", "Printer timeout", PrinterResult.TIMEOUT)
            ]
            
            code, message, result = random.choice(failure_types)
            
            return PrinterResponse(
                status=result.value,
                error_code=code,
                error_message=message
            )
    
    async def _real_receipt_printing(self, request: PrinterRequest) -> PrinterResponse:
        """
        Real printer integration (for future implementation).
        """
        raise NotImplementedError("Real printer integration not implemented yet")
    
    def _generate_pos_terminal_receipt(self, request: PrinterRequest) -> str:
        """Generate realistic POS terminal receipt with ZERO CULTURE branding."""
        payment_data = request.payment_data
        now = datetime.now()
        
        # Extract payment details
        transaction_id = payment_data.get("transaction_id", "TXN_UNKNOWN")
        auth_code = payment_data.get("auth_code", "123456")
        rrn = payment_data.get("rrn", "000010000050")
        amount = payment_data.get("amount", 0)
        terminal_id = payment_data.get("terminal_id", "00092240")
        
        receipt_content = f"""================================
         ZERO CULTURE
================================
POS-Universal
           TEST TEST            
         VTID: XXXXXXX          
ТЕРМИНАЛ №:             {terminal_id}
ДАТА {now.strftime('%d/%m/%y')}     ВРЕМЯ {now.strftime('%H:%M:%S')}
ОПЛАТА ПОКУПКИ
MasterCard    НАЗНАЧЕНИЕ ПЛАТЕЖА
**** **** **** 4340
ПАКЕТ:0000            ЧЕК:{self._receipt_counter:04d}
ПЛАТЕЖНАЯ СИСТЕМА     MasterCard
ТИП КАРТЫ (APP)       Mastercard
             БЕСКОНТАКТНАЯ КАРТА
RRN:{rrn} КОД АВТ.:{auth_code}
AID: A0000000041010        
TVR:8000008001
ИТОГО                 {amount:.2f} RUB
КОД ОТВЕТА                    00
            ОДОБРЕНО            
ПОДПИСЬ КЛИЕНТА НЕ ТРЕБУЕТСЯ


================================
Thank you for your purchase!
================================

Order ID: {request.order_id}
Kiosk: {request.kiosk_id}
Transaction: {transaction_id}
Printed: {now.strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return receipt_content


# Global printer gateway instance
_printer_gateway: Optional[PrinterGateway] = None


def get_printer_gateway() -> PrinterGateway:
    """Get or create printer gateway instance."""
    global _printer_gateway
    if _printer_gateway is None:
        config = PrinterGatewayConfig()
        _printer_gateway = PrinterGateway(config)
    return _printer_gateway


def configure_printer_gateway(config: PrinterGatewayConfig) -> None:
    """Configure printer gateway with custom settings."""
    global _printer_gateway
    _printer_gateway = PrinterGateway(config)
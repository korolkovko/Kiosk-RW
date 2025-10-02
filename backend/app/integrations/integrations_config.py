# integrations_config.py
# Clean configuration for external service integrations - URLs, flags, and basic settings only
# No logic - pure configuration

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class PaymentConfig:
    """Payment gateway configuration - URLs and settings only"""

    # Mode flag
    mockup_mode: bool = False

    # Production service URLs
    gateway_url: str = "https://unified-mocks-service-production.up.railway.app"
    merchant_id: str = ""
    terminal_id: str = ""
    api_key: str = ""
    
    # DC_INPAS specific
    inpas_host: str = ""
    inpas_port: int = 0
    
    # Basic settings
    timeout_seconds: int = 30
    max_retries: int = 3
    use_ssl: bool = True
    
    @classmethod
    def from_env(cls) -> 'PaymentConfig':
        """Load from environment variables"""
        return cls(
            mockup_mode=os.getenv("PAYMENT_MOCKUP", "false").lower() == "true",
            gateway_url=os.getenv("PAYMENT_GATEWAY_URL", "https://unified-mocks-service-production.up.railway.app"),
            merchant_id=os.getenv("PAYMENT_MERCHANT_ID", ""),
            terminal_id=os.getenv("PAYMENT_TERMINAL_ID", ""),
            api_key=os.getenv("PAYMENT_API_KEY", ""),
            inpas_host=os.getenv("INPAS_HOST", ""),
            inpas_port=int(os.getenv("INPAS_PORT", "0")),
            timeout_seconds=int(os.getenv("PAYMENT_TIMEOUT", "30")),
            max_retries=int(os.getenv("PAYMENT_MAX_RETRIES", "3")),
            use_ssl=os.getenv("PAYMENT_USE_SSL", "true").lower() == "true"
        )


@dataclass
class FiscalConfig:
    """Fiscal gateway configuration - URLs and settings only"""

    # Mode flag
    mockup_mode: bool = False

    # Production KKT URLs
    kkt_host: str = "https://unified-mocks-service-production.up.railway.app"
    kkt_port: int = 0
    fiscal_number: str = ""
    inn: str = ""
    ofd_provider: str = ""
    
    # Basic settings
    timeout_seconds: int = 20
    max_retries: int = 2
    use_ssl: bool = True
    fiscal_mode: str = "OSN"
    
    @classmethod
    def from_env(cls) -> 'FiscalConfig':
        """Load from environment variables"""
        return cls(
            mockup_mode=os.getenv("FISCAL_MOCKUP", "false").lower() == "true",
            kkt_host=os.getenv("KKT_HOST", "https://unified-mocks-service-production.up.railway.app"),
            kkt_port=int(os.getenv("KKT_PORT", "0")),
            fiscal_number=os.getenv("FISCAL_NUMBER", ""),
            inn=os.getenv("FISCAL_INN", ""),
            ofd_provider=os.getenv("OFD_PROVIDER", ""),
            timeout_seconds=int(os.getenv("FISCAL_TIMEOUT", "20")),
            max_retries=int(os.getenv("FISCAL_MAX_RETRIES", "2")),
            use_ssl=os.getenv("FISCAL_USE_SSL", "true").lower() == "true",
            fiscal_mode=os.getenv("FISCAL_MODE", "OSN")
        )


@dataclass
class KDSConfig:
    """KDS configuration - URLs and settings only"""

    # Mode flag
    mockup_mode: bool = False

    # Production KDS URLs
    kds_api_url: str = "https://unified-mocks-service-production.up.railway.app"
    kds_api_key: str = ""
    kitchen_station_id: str = ""
    notification_webhook_url: str = ""
    
    # Basic settings
    timeout_seconds: int = 10
    max_retries: int = 2
    use_ssl: bool = True
    auto_confirm_orders: bool = False
    
    @classmethod
    def from_env(cls) -> 'KDSConfig':
        """Load from environment variables"""
        return cls(
            mockup_mode=os.getenv("KDS_MOCKUP", "false").lower() == "true",
            kds_api_url=os.getenv("KDS_API_URL", "https://unified-mocks-service-production.up.railway.app"),
            kds_api_key=os.getenv("KDS_API_KEY", ""),
            kitchen_station_id=os.getenv("KDS_STATION_ID", ""),
            notification_webhook_url=os.getenv("KDS_WEBHOOK_URL", ""),
            timeout_seconds=int(os.getenv("KDS_TIMEOUT", "10")),
            max_retries=int(os.getenv("KDS_MAX_RETRIES", "2")),
            use_ssl=os.getenv("KDS_USE_SSL", "true").lower() == "true",
            auto_confirm_orders=os.getenv("KDS_AUTO_CONFIRM", "false").lower() == "true"
        )


@dataclass
class PrinterConfig:
    """Printer gateway configuration - settings for receipt printing"""

    # Mode flag
    mockup_mode: bool = True

    # File-based printing settings
    receipts_folder: str = "receipts"
    
    # Real printer settings (for future use)
    printer_host: str = ""
    printer_port: int = 0
    printer_model: str = ""
    
    # Basic settings
    timeout_seconds: int = 10
    max_retries: int = 2
    
    @classmethod
    def from_env(cls) -> 'PrinterConfig':
        """Load from environment variables"""
        return cls(
            mockup_mode=os.getenv("PRINTER_MOCKUP", "true").lower() == "true",
            receipts_folder=os.getenv("RECEIPTS_FOLDER", "receipts"),
            printer_host=os.getenv("PRINTER_HOST", ""),
            printer_port=int(os.getenv("PRINTER_PORT", "0")),
            printer_model=os.getenv("PRINTER_MODEL", ""),
            timeout_seconds=int(os.getenv("PRINTER_TIMEOUT", "10")),
            max_retries=int(os.getenv("PRINTER_MAX_RETRIES", "2"))
        )


@dataclass
class IntegrationsConfig:
    """Master configuration for all external services"""
    
    payment: PaymentConfig
    fiscal: FiscalConfig
    kds: KDSConfig
    printer: PrinterConfig
    
    # Global settings
    global_timeout: int = 60
    enable_logging: bool = True
    
    @classmethod
    def from_env(cls) -> 'IntegrationsConfig':
        """Load all configurations from environment"""
        return cls(
            payment=PaymentConfig.from_env(),
            fiscal=FiscalConfig.from_env(),
            kds=KDSConfig.from_env(),
            printer=PrinterConfig.from_env(),
            global_timeout=int(os.getenv("INTEGRATIONS_TIMEOUT", "60")),
            enable_logging=os.getenv("INTEGRATIONS_LOGGING", "true").lower() == "true"
        )


# Global configuration instance
_config: Optional[IntegrationsConfig] = None


def get_integrations_config() -> IntegrationsConfig:
    """Get global integrations configuration"""
    global _config
    if _config is None:
        _config = IntegrationsConfig.from_env()
    return _config


def set_integrations_config(config: IntegrationsConfig) -> None:
    """Set global integrations configuration"""
    global _config
    _config = config


# Environment variables documentation for deployment
ENV_VARS_REQUIRED = {
    "PAYMENT_GATEWAY_URL": "Payment gateway/emulator URL",
    "KKT_HOST": "KKT device/emulator URL", 
    "KDS_API_URL": "Kitchen system/emulator URL"
}

ENV_VARS_OPTIONAL = {
    "PAYMENT_MOCKUP": "true/false - use mockup payment processing",
    "FISCAL_MOCKUP": "true/false - use mockup fiscal processing",
    "KDS_MOCKUP": "true/false - use mockup kitchen processing",
    "PRINTER_MOCKUP": "true/false - use file-based receipt printing",
    "RECEIPTS_FOLDER": "folder path for saving receipt files"
}
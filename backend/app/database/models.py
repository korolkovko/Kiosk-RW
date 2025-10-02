# models.py
# SQLAlchemy ORM models based on the domain model specifications

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text,
    ForeignKey, BigInteger, JSON, Enum as SQLEnum, Date, Time, Numeric
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum
import uuid

from .DomainModel import Base


# Enum definitions based on domain model
class OrderStatus(str, Enum):
    """Order status enumeration"""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class PaymentStatus(str, Enum):
    """Payment status enumeration"""
    AWAITING = "AWAITING"
    DECLINED = "DECLINED"
    ERROR = "ERROR"
    PAID = "PAID"


# PaymentMethodCode enum removed - using String instead for flexibility


class DeviceType(str, Enum):
    """Device type enumeration"""
    KIOSK = "KIOSK"
    POS_TERMINAL = "POS_TERMINAL"
    FISCAL_PRINTER = "FISCAL_PRINTER"
    KKT = "KKT"


class AuthMethod(str, Enum):
    """Customer authentication method enumeration"""
    PSW = "PSW"
    SMS = "SMS"
    QR = "QR"
    NFC_DEVICE = "NFCDevice"
    OAUTH2 = "Oauth2"


# Core domain models
class Role(Base):
    """User access control role"""
    __tablename__ = "roles"
    
    # Primary key
    name = Column(String(100), primary_key=True, unique=True)
    permissions = Column(JSONB, nullable=True)  # JSON permissions structure
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    users = relationship("User", back_populates="role")


class User(Base):
    """Registered user of the system (admin, superadmin, staff)"""
    __tablename__ = "users"
    
    # Primary key
    user_id = Column(Integer, primary_key=True, index=True)
    
    # User identification
    username = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=True)  # Nullable for external auth
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(50), nullable=True, index=True)
    
    # Role relationship
    role_name = Column(String(100), ForeignKey("roles.name"), nullable=False)
    
    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    role = relationship("Role", back_populates="users")
    created_items = relationship("ItemLive", back_populates="creator", foreign_keys="ItemLive.created_by")
    stock_changes = relationship("ItemLiveStockReplenishment", back_populates="user")
    sessions = relationship("Session", back_populates="user")


class KnownCustomer(Base):
    """Identified customer using the kiosk"""
    __tablename__ = "known_customers"
    
    # Primary key
    customer_id = Column(BigInteger, primary_key=True, index=True)
    
    # Customer information
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(50), nullable=True, index=True)
    
    # Loyalty and authentication
    loyalty_card_code = Column(String(100), nullable=True, unique=True)
    auth_method = Column(SQLEnum(AuthMethod), nullable=True)
    
    # Customer lifecycle
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_seen_at = Column(DateTime(timezone=True), nullable=True)
    is_anonymous_link = Column(Boolean, default=False, nullable=True)
    
    # Relationships
    orders = relationship("Order", back_populates="customer")
    sessions = relationship("Session", back_populates="customer")


class Session(Base):
    """Active user or kiosk session"""
    __tablename__ = "sessions"
    
    # Primary key
    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Session participants (nullable for anonymous sessions)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    device_id = Column(Integer, ForeignKey("devices.device_id"), nullable=True)
    customer_id = Column(BigInteger, ForeignKey("known_customers.customer_id"), nullable=True)
    
    # Session lifecycle
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active_at = Column(DateTime(timezone=True), server_default=func.now())
    expired_at = Column(DateTime(timezone=True), nullable=True)
    
    # Session token
    session_token = Column(String(500), nullable=True, index=True)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    device = relationship("Device", back_populates="sessions")
    customer = relationship("KnownCustomer", back_populates="sessions")
    orders = relationship("Order", back_populates="session")


class UnitOfMeasure(Base):
    """Register of measurement units"""
    __tablename__ = "units_of_measure"
    
    # Primary key
    name_eng = Column(String(100), primary_key=True, index=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    items = relationship("ItemLive", back_populates="unit_measure")


class FoodCategory(Base):
    """Food item categories (Drinks, Meals, Sauces, etc.)"""
    __tablename__ = "food_categories"
    
    # Primary key
    name = Column(String(100), primary_key=True, unique=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    items = relationship("ItemLive", back_populates="food_category")


class DayCategory(Base):
    """Time-based classifications (Breakfast, Lunch, Dinner, etc.)"""
    __tablename__ = "day_categories"
    
    # Primary key
    name = Column(String(100), primary_key=True, unique=True)
    
    # Time range
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    items = relationship("ItemLive", back_populates="day_category")


class ItemLive(Base):
    """Active menu items available for ordering"""
    __tablename__ = "items_live"
    
    # Primary key
    item_id = Column(BigInteger, primary_key=True, index=True)
    
    # Item names and descriptions
    name_ru= Column(String(200), nullable=False)
    name_eng = Column(String(200), nullable=True)
    description_ru = Column(Text, nullable=False)
    description_eng = Column(Text, nullable=True)
    
    # Item status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Unit of measure relationships
    unit_measure_name_eng = Column(String(100), ForeignKey("units_of_measure.name_eng"), nullable=False)
    
    # Pricing
    price_net = Column(Numeric(10, 2), nullable=False)
    vat_rate = Column(Numeric(5, 2), nullable=True)
    vat_amount = Column(Numeric(10, 2), nullable=False)
    price_gross = Column(Numeric(10, 2), nullable=False)
    
    # Categories
    food_category_name = Column(String(100), ForeignKey("food_categories.name"), nullable=False)
    day_category_name = Column(String(100), ForeignKey("day_categories.name"), nullable=False)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    
    # Relationships
    creator = relationship("User", back_populates="created_items", foreign_keys=[created_by])
    unit_measure = relationship("UnitOfMeasure", back_populates="items")
    food_category = relationship("FoodCategory", back_populates="items")
    day_category = relationship("DayCategory", back_populates="items")
    availability = relationship("ItemLiveAvailable", back_populates="item", uselist=False)
    stock_changes = relationship("ItemLiveStockReplenishment", back_populates="item")


class ItemLiveAvailable(Base):
    """Current stock availability for active items"""
    __tablename__ = "items_live_available"
    
    # Primary key (also foreign key to ItemLive)
    item_id = Column(BigInteger, ForeignKey("items_live.item_id", ondelete="CASCADE"), 
                     primary_key=True, index=True)
    
    # Stock quantities
    stock_quantity = Column(Integer, nullable=False, default=0)
    reserved_quantity = Column(Integer, nullable=False, default=0)
    
    # Unit snapshots from ItemLive
    unit_name_ru = Column(String(100), nullable=False)
    unit_name_eng = Column(String(100), nullable=True)
    
    # Relationships
    item = relationship("ItemLive", back_populates="availability")


class ItemLiveStockReplenishment(Base):
    """Stock replenishment history for items"""
    __tablename__ = "items_live_stock_replenishment"
    
    # Primary key
    operation_id = Column(BigInteger, primary_key=True, index=True)
    
    # Item reference
    item_id = Column(BigInteger, ForeignKey("items_live.item_id", ondelete="CASCADE"), 
                     nullable=False, index=True)
    
    # Item snapshots at time of operation
    name_ru = Column(String(200), nullable=False)
    description_ru = Column(Text, nullable=False)
    unit_name_ru = Column(String(100), nullable=False)
    unit_name_eng = Column(String(100), nullable=True)
    
    # Stock change
    change_quantity = Column(Integer, nullable=False)
    
    # Audit fields
    changed_at = Column(DateTime(timezone=True), server_default=func.now())
    changed_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    
    # Relationships
    item = relationship("ItemLive", back_populates="stock_changes")
    user = relationship("User", back_populates="stock_changes")


class Device(Base):
    """Registered hardware devices (kiosk, POS, fiscal printer, etc.)"""
    __tablename__ = "devices"
    
    # Primary key
    device_id = Column(Integer, primary_key=True, index=True)
    
    # Device identification
    device_type = Column(SQLEnum(DeviceType), nullable=False)
    device_code = Column(String(50), nullable=False, unique=True, index=True)
    device_name = Column(String(200), nullable=False)
    
    # Location
    branch_name = Column(String(200), ForeignKey("branches.name"), nullable=True)
    
    # Network information
    ip_address = Column(String(45), nullable=True)  # IPv4/IPv6
    mac_address = Column(String(17), nullable=True)
    
    # Hardware information
    serial_number = Column(String(100), nullable=True)
    firmware_version = Column(String(50), nullable=True)
    device_os = Column(String(50), nullable=True)
    
    # Device status
    is_managed = Column(Boolean, default=True, nullable=True)
    is_active = Column(Boolean, default=True, nullable=True)
    last_heartbeat = Column(DateTime(timezone=True), nullable=True)
    
    # Audit fields
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    branch = relationship("Branch", back_populates="devices")
    sessions = relationship("Session", back_populates="device")
    pos_terminal = relationship("POSTerminal", back_populates="device", uselist=False)
    fiscal_device = relationship("FiscalDevice", back_populates="device", uselist=False)


class Branch(Base):
    """Restaurant branch/location settings"""
    __tablename__ = "branches"
    
    # Primary key
    name = Column(String(200), primary_key=True)
    address = Column(JSONB, nullable=False)  # Structured address data
    work_hours = Column(JSONB, nullable=False)  # Operating hours structure
    legal_entity = Column(JSONB, nullable=False)  # Legal and tax information
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    devices = relationship("Device", back_populates="branch")


class Order(Base):
    """Customer orders/transactions"""
    __tablename__ = "orders"
    
    # Primary key
    order_id = Column(BigInteger, primary_key=True, index=True)
    order_date = Column(Date, nullable=False, index=True)
    
    # Order status and timing
    status = Column(SQLEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    order_time = Column(DateTime(timezone=True), server_default=func.now())
    
    # Financial information
    currency = Column(String(3), nullable=False, default="RUB")
    total_amount_net = Column(Numeric(10, 2), nullable=False)
    total_amount_vat = Column(Numeric(10, 2), nullable=False)
    total_amount_gross = Column(Numeric(10, 2), nullable=False)
    
    # Customer and session
    customer_id = Column(BigInteger, ForeignKey("known_customers.customer_id"), nullable=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.session_id"), nullable=True)
    
    # Pickup information
    pickup_number = Column(String(20), nullable=False, index=True)
    pin_code = Column(String(10), nullable=False)
    
    # Device snapshots (from session time)
    kiosk_id = Column(Integer, nullable=True)
    kiosk_ip = Column(String(45), nullable=True)
    kiosk_port = Column(String(10), nullable=True)
    pos_terminal_id = Column(Integer, nullable=True)
    pos_terminal_ip = Column(String(45), nullable=True)
    pos_terminal_port = Column(String(10), nullable=True)
    fiscal_machine_id = Column(Integer, nullable=True)
    fiscal_machine_ip = Column(String(45), nullable=True)
    fiscal_machine_port = Column(String(10), nullable=True)
    fiscal_printer_id = Column(Integer, nullable=True)
    fiscal_printer_ip = Column(String(45), nullable=True)
    fiscal_printer_port = Column(String(10), nullable=True)
    
    # Relationships
    customer = relationship("KnownCustomer", back_populates="orders")
    session = relationship("Session", back_populates="orders")
    payments = relationship("Payment", back_populates="order")


class Payment(Base):
    """Payment details for orders"""
    __tablename__ = "payments"
    
    # Primary key
    payment_id = Column(BigInteger, primary_key=True, index=True)
    
    # Order reference
    order_id = Column(BigInteger, ForeignKey("orders.order_id"), nullable=False, index=True)
    
    # Payment timing
    payment_date = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Financial details
    currency = Column(String(3), nullable=True, default="RUB")
    total_amount_net = Column(Numeric(10, 2), nullable=False)
    vat_rate = Column(Numeric(5, 2), nullable=False)
    total_amount_vat = Column(Numeric(10, 2), nullable=False)
    total_amount_gross = Column(Numeric(10, 2), nullable=False)
    
    # Payment method and status
    method_code = Column(String(50), ForeignKey("payment_methods.code"), nullable=True)
    status = Column(SQLEnum(PaymentStatus), nullable=True, default=PaymentStatus.AWAITING)
    
    # Transaction details
    transaction_id = Column(String(100), nullable=True, index=True)
    payment_details = Column(Text, nullable=True)
    pos_terminal_id = Column(Integer, nullable=True)
    
    # Response information
    response_code = Column(String(10), nullable=True)
    response_message = Column(String(500), nullable=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    order = relationship("Order", back_populates="payments")
    method = relationship("PaymentMethod", back_populates="payments")


class PaymentMethod(Base):
    """Available payment methods"""
    __tablename__ = "payment_methods"
    
    # Primary key
    code = Column(String(50), primary_key=True, unique=True)
    description_ru = Column(String(200), nullable=False)
    description_en = Column(String(200), nullable=False)
    
    # Method status
    is_active = Column(Boolean, default=True, nullable=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    payments = relationship("Payment", back_populates="method")


class POSTerminal(Base):
    """POS terminal specific configuration"""
    __tablename__ = "pos_terminals"
    
    # Primary key (also foreign key to Device)
    terminal_id = Column(Integer, ForeignKey("devices.device_id"), primary_key=True)
    
    # Banking details
    bank_terminal_id = Column(String(50), nullable=False)
    merchant_id = Column(String(50), nullable=True)
    bank_name = Column(String(100), nullable=True)
    
    # Terminal configuration
    supported_card_types = Column(JSONB, nullable=True)  # List of supported card types
    min_amount = Column(Numeric(10, 2), nullable=True)
    max_amount = Column(Numeric(10, 2), nullable=True)
    commission_rate = Column(Numeric(5, 2), nullable=True)
    
    # Relationships
    device = relationship("Device", back_populates="pos_terminal")


class FiscalDevice(Base):
    """Fiscal printer/KKT configuration"""
    __tablename__ = "fiscal_devices"
    
    # Primary key (also foreign key to Device)
    fiscal_id = Column(Integer, ForeignKey("devices.device_id"), primary_key=True)
    
    # Fiscal details
    fiscal_number = Column(String(50), nullable=False)
    inn = Column(String(12), nullable=False)  # Russian tax ID
    fiscal_mode = Column(String(20), nullable=True)  # OSN, USN, ENVD
    
    # OFD integration
    ofd_provider = Column(String(100), nullable=True)
    certificate_expiry = Column(Date, nullable=True)
    last_fiscal_report = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    device = relationship("Device", back_populates="fiscal_device")
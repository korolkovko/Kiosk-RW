# ItemLiveAddPydanticModel.py
# Pydantic models for LiveItem creation API

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import datetime


class ItemLiveCreateRequest(BaseModel):
    """Request model for creating new LiveItem"""
    name_ru: str = Field(..., min_length=1, max_length=200, description="Russian name")
    name_eng: Optional[str] = Field(None, max_length=200, description="English name")
    description_ru: str = Field(..., min_length=1, description="Russian description")
    description_eng: Optional[str] = Field(None, description="English description")

    # Unit and categories (required)
    unit_measure_name_eng: str = Field(..., description="Unit of measure name (English)")
    food_category_name: str = Field(..., description="Food category name")
    day_category_name: str = Field(..., description="Day category name")

    # Pricing
    price_net: Decimal = Field(..., gt=0, description="Net price without VAT")
    vat_rate: Optional[Decimal] = Field(None, ge=0, le=100, description="VAT rate %")
    vat_amount: Decimal = Field(..., ge=0, description="Calculated VAT amount")
    price_gross: Decimal = Field(..., gt=0, description="Total price including VAT")

    # Status
    is_active: bool = Field(True, description="Item active status")

    model_config = ConfigDict(
        json_encoders={Decimal: lambda v: str(v)},
        json_schema_extra={
            "example": {
                "name_ru": "Кофе эспрессо",
                "name_eng": "Espresso Coffee",
                "description_ru": "Классический итальянский эспрессо",
                "description_eng": "Classic Italian espresso",
                "unit_measure_name_eng": "piece",
                "food_category_name": "Drinks",
                "day_category_name": "All Day",
                "price_net": "2.50",
                "vat_rate": "20.0",
                "vat_amount": "0.50",
                "price_gross": "3.00",
                "is_active": True
            }
        }
    )


class ItemLiveResponse(BaseModel):
    """Response model for created LiveItem"""
    item_id: int
    name_ru: str
    name_eng: Optional[str]
    description_ru: str
    description_eng: Optional[str]

    unit_measure_name_eng: str
    food_category_name: str
    day_category_name: str

    price_net: Decimal
    vat_rate: Optional[Decimal]
    vat_amount: Decimal
    price_gross: Decimal

    is_active: bool
    created_at: datetime
    created_by: int

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={Decimal: lambda v: str(v)}
    )
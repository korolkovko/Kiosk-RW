# ItemUpdatePropertiesDBCRUD.py
# Database CRUD operations for updating LiveItem properties (description, price, VAT, categories, etc.)

from sqlalchemy.orm import Session
from typing import Optional

from ..database.models import ItemLive, UnitOfMeasure, FoodCategory, DayCategory
from ..models.ItemUpdatePropertiesPydanticModel import ItemUpdatePropertiesRequest

class ItemUpdatePropertiesDBCRUD:
    """Database CRUD operations for updating LiveItem properties"""

    def get_item(self, db: Session, item_id: int) -> Optional[ItemLive]:
        """Fetch LiveItem by ID"""
        return db.query(ItemLive).filter(ItemLive.item_id == item_id).first()

    def validate_unit_exists(self, db: Session, unit_name_eng: str) -> Optional[UnitOfMeasure]:
        """Check if unit exists"""
        return db.query(UnitOfMeasure).filter(UnitOfMeasure.name_eng == unit_name_eng).first()

    def validate_food_category_exists(self, db: Session, category_name: str) -> Optional[FoodCategory]:
        """Check if food category exists"""
        return db.query(FoodCategory).filter(FoodCategory.name == category_name).first()

    def validate_day_category_exists(self, db: Session, category_name: str) -> Optional[DayCategory]:
        """Check if day category exists"""
        return db.query(DayCategory).filter(DayCategory.name == category_name).first()

    def update_item(self, db: Session, item: ItemLive, update_data: ItemUpdatePropertiesRequest) -> ItemLive:
        """Update LiveItem fields based on provided data"""
        if update_data.name_ru is not None:
            item.name_ru = update_data.name_ru
        if update_data.name_eng is not None:
            item.name_eng = update_data.name_eng
        if update_data.description_ru is not None:
            item.description_ru = update_data.description_ru
        if update_data.description_eng is not None:
            item.description_eng = update_data.description_eng
        if update_data.unit_measure_name_eng is not None:
            item.unit_measure_name_eng = update_data.unit_measure_name_eng
        if update_data.food_category_name is not None:
            item.food_category_name = update_data.food_category_name
        if update_data.day_category_name is not None:
            item.day_category_name = update_data.day_category_name
        if update_data.price_net is not None:
            item.price_net = update_data.price_net
        if update_data.vat_rate is not None:
            item.vat_rate = update_data.vat_rate
        if update_data.vat_amount is not None:
            item.vat_amount = update_data.vat_amount
        if update_data.price_gross is not None:
            item.price_gross = update_data.price_gross

        db.flush()
        return item

# Global service instance
item_update_properties_db_crud = ItemUpdatePropertiesDBCRUD()
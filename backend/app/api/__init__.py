# __init__.py
# API module initialization

from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .superadminfirstcreation import router as setup_router
from .ItemLiveAddEndPoint import router as item_live_add_router
from .ItemLiveStockReplenishmentEndPoint import router as item_live_stock_replenishment_router
from .ItemStopListEndPoint import router as item_stop_list_router
from .ItemUpdatePropertiesEndPoint import router as item_update_properties_router
from .GetAllItemLiveEndPoint import router as get_all_item_live_router

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(setup_router)  # First-time setup endpoints
api_router.include_router(auth_router)   # Standard authentication endpoints
api_router.include_router(users_router)  # User management endpoints
api_router.include_router(item_live_add_router)  # Item live add endpoints
api_router.include_router(item_live_stock_replenishment_router)  # Stock replenish/remove endpoints
api_router.include_router(item_stop_list_router)  # Stop list endpoints
api_router.include_router(item_update_properties_router)  # Update item properties endpoint
api_router.include_router(get_all_item_live_router)       # Get all live items endpoint

__all__ = ["api_router"]
from pydantic import BaseModel
from typing import Optional
from datetime import date


# =========================================================
# FARMER
# =========================================================

class FarmerCreate(BaseModel):

    name: str
    mobile: str
    password: str
    farm_location: str


class FarmerLogin(BaseModel):

    mobile: str
    password: str
# =========================================================
# CUSTOMER REGISTRATION
# =========================================================

class CustomerCreate(BaseModel):

    name: str

    mobile: str

    password: str

    location: str


# =========================================================
# CUSTOMER LOGIN
# =========================================================

class CustomerLogin(BaseModel):

    mobile: str

    password: str

# =========================================================
# WHOLESALER
# =========================================================

class WholesalerCreate(BaseModel):

    company_name: str
    email: str
    password: str
    company_location: str


class WholesalerLogin(BaseModel):

    email: str
    password: str


# =========================================================
# CROP SLOT
# =========================================================

class CropSlotCreate(BaseModel):

    farmer_id: int

    farmer_name: str

    mobile: str

    farm_location: str

    crop_name: str

    crop_type: str

    quantity: float

    quantity_unit: str

    expected_price: float

    price_unit: str

    available_date: date

    slot_closing_date: date

    quality: str

    moisture: Optional[str] = None

    additional_requirements: Optional[str] = None


# =========================================================
# BID
# =========================================================

class BidCreate(BaseModel):

    wholesaler_id: int

    crop_slot_id: int

    company_name: str

    company_location: str

    crop_name: str

    crop_type: Optional[str] = None

    quantity: float

    quantity_unit: str

    bid_price: float

    price_unit: str

    required_date: date

    bid_closing_date: date

    quality: str

    moisture: Optional[float] = None

    additional_requirements: Optional[str] = None


# =========================================================
# BID RESPONSE
# =========================================================

class BidResponseCreate(BaseModel):

    bid_id: int

    farmer_id: int

    farmer_name: str

    crop_slot_id: int

    offered_price: float

    quantity: float


# =========================================================
# MARKET PRICE
# =========================================================

class MarketPriceCreate(BaseModel):

    crop_name: str

    market_name: str

    location: str

    price: float

    price_unit: str

    date: date
from sqlalchemy import Column, Integer, String, Float, Text, Date

from database import Base


# =========================================================
# FARMER TABLE
# =========================================================

class Farmer(Base):



    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    mobile = Column(String(15), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    farm_location = Column(String(200), nullable=False)

# =========================================================
# CUSTOMER TABLE
# =========================================================

class Customer(Base):

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    mobile = Column(String(15), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    location = Column(String(200), nullable=False)
# =========================================================
# WHOLESALER TABLE
# =========================================================



class Wholesaler(Base):

    __tablename__ = "wholesalers"

    id = Column(Integer, primary_key=True, index=True)

    company_name = Column(String(150), nullable=False)

    email = Column(String(150), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    company_location = Column(String(200), nullable=False)


# =========================================================
# CROP SLOT TABLE
# =========================================================



class CropSlot(Base):

    __tablename__ = "crop_slots"

    id = Column(Integer, primary_key=True, index=True)

    farmer_id = Column(Integer, nullable=False)

    farmer_name = Column(String(100), nullable=False)

    mobile = Column(String(15), nullable=False)

    farm_location = Column(String(200), nullable=False)

    crop_name = Column(String(100), nullable=False)

    crop_type = Column(String(100), nullable=False)

    quantity = Column(Float, nullable=False)

    quantity_unit = Column(String(30), nullable=False)

    expected_price = Column(Float, nullable=False)

    price_unit = Column(String(30), nullable=False)

    available_date = Column(Date, nullable=False)

    slot_closing_date = Column(Date, nullable=False)

    quality = Column(String(100), nullable=False)

    moisture = Column(String(30), nullable=True)

    additional_requirements = Column(Text, nullable=True)

    status = Column(String(30), default="Available")


# =========================================================
# BID TABLE
# =========================================================

class Bid(Base):

    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)

    # Wholesaler who created the bid
    wholesaler_id = Column(Integer, nullable=False)

    # Farmer crop slot for which bid is created
    crop_slot_id = Column(Integer, nullable=False)

    company_name = Column(String(150), nullable=False)

    company_location = Column(String(200), nullable=False)

    crop_name = Column(String(100), nullable=False)

    crop_type = Column(String(100), nullable=True)

    quantity = Column(Float, nullable=False)

    quantity_unit = Column(String(30), nullable=False)

    bid_price = Column(Float, nullable=False)

    price_unit = Column(String(30), nullable=False)

    required_date = Column(Date, nullable=False)

    bid_closing_date = Column(Date, nullable=False)

    quality = Column(String(50), nullable=False)

    moisture = Column(Float, nullable=True)

    additional_requirements = Column(Text, nullable=True)

    status = Column(String(30), default="Active")


# =========================================================
# BID RESPONSE TABLE
# =========================================================

class BidResponse(Base):

    __tablename__ = "bid_responses"

    id = Column(Integer, primary_key=True, index=True)

    bid_id = Column(Integer, nullable=False)

    farmer_id = Column(Integer, nullable=False)

    farmer_name = Column(String(100), nullable=False)

    crop_slot_id = Column(Integer, nullable=False)

    offered_price = Column(Float, nullable=False)

    quantity = Column(Float, nullable=False)

    status = Column(String(30), default="Pending")


# =========================================================
# MARKET PRICE TABLE
# =========================================================

class MarketPrice(Base):

    __tablename__ = "market_prices"

    id = Column(Integer, primary_key=True, index=True)

    crop_name = Column(String(100), nullable=False)

    market_name = Column(String(150), nullable=False)

    location = Column(String(150), nullable=False)

    price = Column(Float, nullable=False)

    price_unit = Column(String(30), nullable=False)

    date = Column(Date, nullable=False)
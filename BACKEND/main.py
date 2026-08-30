from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
from database import engine, get_db

from schemas import (
    FarmerCreate,
    FarmerLogin,
    WholesalerCreate,
    WholesalerLogin,
    CustomerCreate,
    CustomerLogin,
    CropSlotCreate,
    BidCreate,
    BidResponseCreate,
    MarketPriceCreate
)


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

models.Base.metadata.create_all(bind=engine)


# =========================================================
# CREATE FASTAPI APP
# =========================================================

app = FastAPI(
    title="Krishi Connect API",
    description="Agricultural marketplace backend",
    version="1.0.0"
)

@app.on_event("startup")
def run_import_on_startup():
    from database import SessionLocal
    from models import MarketPrice

    db = SessionLocal()
    count = db.query(MarketPrice).count()
    db.close()

    if count == 0:
        import subprocess
        subprocess.run(["python", "import_data.py"])
# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "Krishi Connect Backend is running",
        "status": "success"
    }


# =========================================================
# FARMER REGISTRATION
# =========================================================

@app.post("/api/farmers/register")
def register_farmer(
    farmer: FarmerCreate,
    db: Session = Depends(get_db)
):

    existing_farmer = db.query(
        models.Farmer
    ).filter(
        models.Farmer.mobile == farmer.mobile
    ).first()

    if existing_farmer:

        raise HTTPException(
            status_code=400,
            detail="Farmer with this mobile number already exists"
        )

    new_farmer = models.Farmer(

        name=farmer.name,

        mobile=farmer.mobile,

        password=farmer.password,

        farm_location=farmer.farm_location
    )

    db.add(new_farmer)

    db.commit()

    db.refresh(new_farmer)

    return {

        "message": "Farmer registered successfully",

        "farmer_id": new_farmer.id
    }


# =========================================================
# FARMER LOGIN
# =========================================================

@app.post("/api/farmers/login")
def farmer_login(
    farmer: FarmerLogin,
    db: Session = Depends(get_db)
):

    existing_farmer = db.query(
        models.Farmer
    ).filter(

        models.Farmer.mobile == farmer.mobile,

        models.Farmer.password == farmer.password

    ).first()

    if not existing_farmer:

        raise HTTPException(
            status_code=401,
            detail="Invalid mobile number or password"
        )

    return {

        "message": "Farmer login successful",

        "farmer_id": existing_farmer.id,

        "name": existing_farmer.name,

        "mobile": existing_farmer.mobile,

        "farm_location":
            existing_farmer.farm_location
    }
# =========================================================
# CUSTOMER REGISTRATION
# =========================================================

@app.post("/api/customers/register")
def register_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):

    existing_customer = db.query(
        models.Customer
    ).filter(
        models.Customer.mobile == customer.mobile
    ).first()

    if existing_customer:

        raise HTTPException(
            status_code=400,
            detail="Customer with this mobile number already exists"
        )

    new_customer = models.Customer(

        name=customer.name,

        mobile=customer.mobile,

        password=customer.password,

        location=customer.location
    )

    db.add(new_customer)

    db.commit()

    db.refresh(new_customer)

    return {

        "message": "Customer registered successfully",

        "customer_id": new_customer.id
    }


# =========================================================
# CUSTOMER LOGIN
# =========================================================

@app.post("/api/customers/login")
def customer_login(
    customer: CustomerLogin,
    db: Session = Depends(get_db)
):

    existing_customer = db.query(
        models.Customer
    ).filter(

        models.Customer.mobile == customer.mobile,

        models.Customer.password == customer.password

    ).first()

    if not existing_customer:

        raise HTTPException(
            status_code=401,
            detail="Invalid mobile number or password"
        )

    return {

        "message": "Customer login successful",

        "customer_id": existing_customer.id,

        "name": existing_customer.name,

        "mobile": existing_customer.mobile,

        "location": existing_customer.location
    }

# =========================================================
# WHOLESALER REGISTRATION
# =========================================================

@app.post("/api/wholesalers/register")
def register_wholesaler(
    wholesaler: WholesalerCreate,
    db: Session = Depends(get_db)
):

    existing_wholesaler = db.query(
        models.Wholesaler
    ).filter(
        models.Wholesaler.email == wholesaler.email
    ).first()

    if existing_wholesaler:

        raise HTTPException(
            status_code=400,
            detail="Wholesaler with this email already exists"
        )

    new_wholesaler = models.Wholesaler(

        company_name=wholesaler.company_name,

        email=wholesaler.email,

        password=wholesaler.password,

        company_location=wholesaler.company_location
    )

    db.add(new_wholesaler)

    db.commit()

    db.refresh(new_wholesaler)

    return {

        "message": "Wholesaler registered successfully",

        "wholesaler_id": new_wholesaler.id
    }


# =========================================================
# WHOLESALER LOGIN
# =========================================================

@app.post("/api/wholesalers/login")
def wholesaler_login(
    wholesaler: WholesalerLogin,
    db: Session = Depends(get_db)
):

    existing_wholesaler = db.query(
        models.Wholesaler
    ).filter(

        models.Wholesaler.email == wholesaler.email,

        models.Wholesaler.password == wholesaler.password

    ).first()

    if not existing_wholesaler:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {

        "message": "Wholesaler login successful",

        "wholesaler_id": existing_wholesaler.id,

        "company_name":
            existing_wholesaler.company_name,

        "email":
            existing_wholesaler.email,

        "company_location":
            existing_wholesaler.company_location
    }


# =========================================================
# CREATE CROP SLOT
# =========================================================

@app.post("/api/crop-slots/create")
def create_crop_slot(
    slot: CropSlotCreate,
    db: Session = Depends(get_db)
):

    farmer = db.query(
        models.Farmer
    ).filter(
        models.Farmer.id == slot.farmer_id
    ).first()

    if not farmer:

        raise HTTPException(
            status_code=404,
            detail="Farmer not found"
        )

    new_slot = models.CropSlot(

        farmer_id=slot.farmer_id,

        farmer_name=slot.farmer_name,

        mobile=slot.mobile,

        farm_location=slot.farm_location,

        crop_name=slot.crop_name,

        crop_type=slot.crop_type,

        quantity=slot.quantity,

        quantity_unit=slot.quantity_unit,

        expected_price=slot.expected_price,

        price_unit=slot.price_unit,

        available_date=slot.available_date,

        slot_closing_date=slot.slot_closing_date,

        quality=slot.quality,

        moisture=slot.moisture,

        additional_requirements=
            slot.additional_requirements,

        status="Available"
    )

    db.add(new_slot)

    db.commit()

    db.refresh(new_slot)

    return {

        "message": "Crop slot created successfully",

        "crop_slot_id": new_slot.id
    }



# =========================================================
# GET ALL CROP SLOTS
# =========================================================
# IMPORTANT:
# Create Bid page uses this endpoint.

@app.get("/api/crop-slots")
def get_all_crop_slots(
    db: Session = Depends(get_db)
):
    slots = db.query(
        models.CropSlot
    ).filter(
        models.CropSlot.status == "Available"
    ).all()

    return slots


# =========================================================
# GET ONE CROP SLOT
# =========================================================

@app.get("/api/crop-slots/{slot_id}")
def get_one_crop_slot(
    slot_id: int,
    db: Session = Depends(get_db)
):

    slot = db.query(
        models.CropSlot
    ).filter(
        models.CropSlot.id == slot_id
    ).first()

    if not slot:

        raise HTTPException(
            status_code=404,
            detail="Crop slot not found"
        )

    return slot


# =========================================================
# GET ONE FARMER'S CROP SLOTS
# =========================================================

@app.get("/api/farmers/{farmer_id}/crop-slots")
def get_farmer_crop_slots(
    farmer_id: int,
    db: Session = Depends(get_db)
):

    slots = db.query(
        models.CropSlot
    ).filter(
        models.CropSlot.farmer_id == farmer_id
    ).all()

    return slots


# =========================================================
# CREATE WHOLESALER BID
# =========================================================

@app.post("/api/bids/create")
def create_bid(
    bid: BidCreate,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------------
    # CHECK WHOLESALER
    # -----------------------------------------------------

    wholesaler = db.query(
        models.Wholesaler
    ).filter(
        models.Wholesaler.id == bid.wholesaler_id
    ).first()

    if not wholesaler:

        raise HTTPException(
            status_code=404,
            detail="Wholesaler not found"
        )


    # -----------------------------------------------------
    # CHECK CROP SLOT
    # -----------------------------------------------------

    crop_slot = db.query(
        models.CropSlot
    ).filter(
        models.CropSlot.id == bid.crop_slot_id
    ).first()

    if not crop_slot:

        raise HTTPException(
            status_code=404,
            detail="Selected farmer crop slot not found"
        )


    # -----------------------------------------------------
    # CHECK SLOT STATUS
    # -----------------------------------------------------

    if crop_slot.status != "Available":

        raise HTTPException(
            status_code=400,
            detail="Selected crop slot is not available"
        )


    # -----------------------------------------------------
    # CREATE BID
    # -----------------------------------------------------

    new_bid = models.Bid(

        wholesaler_id=bid.wholesaler_id,

        # IMPORTANT:
        # Save farmer crop slot ID
        crop_slot_id=bid.crop_slot_id,

        company_name=bid.company_name,

        company_location=bid.company_location,

        crop_name=bid.crop_name,

        crop_type=bid.crop_type,

        quantity=bid.quantity,

        quantity_unit=bid.quantity_unit,

        bid_price=bid.bid_price,

        price_unit=bid.price_unit,

        required_date=bid.required_date,

        bid_closing_date=bid.bid_closing_date,

        quality=bid.quality,

        moisture=bid.moisture,

        additional_requirements=
            bid.additional_requirements,

        status="Active"
    )


    db.add(new_bid)

    db.commit()

    db.refresh(new_bid)


    return {

        "message": "Bid created successfully",

        "bid_id": new_bid.id,

        "crop_slot_id": new_bid.crop_slot_id
    }


# =========================================================
# GET ALL WHOLESALER BIDS
# =========================================================

@app.get("/api/bids")
def get_all_bids(
    db: Session = Depends(get_db)
):

    bids = db.query(
        models.Bid
    ).all()

    return bids


# =========================================================
# GET ONE WHOLESALER'S BIDS
# =========================================================

@app.get("/api/wholesalers/{wholesaler_id}/bids")
def get_wholesaler_bids(
    wholesaler_id: int,
    db: Session = Depends(get_db)
):

    bids = db.query(
        models.Bid
    ).filter(
        models.Bid.wholesaler_id == wholesaler_id
    ).all()

    return bids


# =========================================================
# FARMER RESPONDS TO BID
# =========================================================

@app.post("/api/bid-responses/create")
def respond_to_bid(
    response: BidResponseCreate,
    db: Session = Depends(get_db)
):

    bid = db.query(
        models.Bid
    ).filter(
        models.Bid.id == response.bid_id
    ).first()

    if not bid:

        raise HTTPException(
            status_code=404,
            detail="Bid not found"
        )

    farmer = db.query(
        models.Farmer
    ).filter(
        models.Farmer.id == response.farmer_id
    ).first()

    if not farmer:

        raise HTTPException(
            status_code=404,
            detail="Farmer not found"
        )

    new_response = models.BidResponse(

        bid_id=response.bid_id,

        farmer_id=response.farmer_id,

        farmer_name=response.farmer_name,

        crop_slot_id=response.crop_slot_id,

        offered_price=response.offered_price,

        quantity=response.quantity,

        status="Pending"
    )

    db.add(new_response)

    db.commit()

    db.refresh(new_response)

    return {

        "message": "Bid response submitted successfully",

        "response_id": new_response.id
    }


# =========================================================
# GET BID RESPONSES
# =========================================================

@app.get("/api/bids/{bid_id}/responses")
def get_bid_responses(
    bid_id: int,
    db: Session = Depends(get_db)
):

    responses = db.query(
        models.BidResponse
    ).filter(
        models.BidResponse.bid_id == bid_id
    ).all()

    return responses


# =========================================================
# ADD MARKET PRICE
# =========================================================

@app.post("/api/market-prices/create")
def create_market_price(
    market_price: MarketPriceCreate,
    db: Session = Depends(get_db)
):

    new_price = models.MarketPrice(

        crop_name=market_price.crop_name,

        market_name=market_price.market_name,

        location=market_price.location,

        price=market_price.price,

        price_unit=market_price.price_unit,

        date=market_price.date
    )

    db.add(new_price)

    db.commit()

    db.refresh(new_price)

    return {

        "message": "Market price added successfully",

        "market_price_id": new_price.id
    }


# =========================================================
# GET MARKET PRICES
# =========================================================

@app.get("/api/market-prices")
def get_market_prices(
    db: Session = Depends(get_db)
):

    prices = db.query(
        models.MarketPrice
    ).all()

    return prices
@app.get("/api/market-prices/search")
def search_market_prices(
    commodity: str = None,
    market: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(models.MarketPrice)

    if commodity:
        query = query.filter(
            models.MarketPrice.crop_name.ilike(
                f"%{commodity}%"
            )
        )

    if market:
        query = query.filter(
            models.MarketPrice.market_name.ilike(
                f"%{market}%"
            )
        )

    prices = query.order_by(
        models.MarketPrice.date.desc()
    ).limit(50).all()

    return prices
# =========================================================
# GET ALL WHOLESALERS - TEST
# =========================================================

@app.get("/api/wholesalers")
def get_all_wholesalers(
    db: Session = Depends(get_db)
):

    wholesalers = db.query(
        models.Wholesaler
    ).all()

    return wholesalers

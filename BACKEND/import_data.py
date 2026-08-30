
import os
import pandas as pd

from database import SessionLocal
from models import MarketPrice


# =========================================================
# START
# =========================================================

print("================================")
print("Starting market data import")
print("================================")


# =========================================================
# CSV FILE PATH
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

file_path = os.path.join(
    BASE_DIR,
    "Data",
    "market_prices.csv"
)

print("CSV file:")
print(file_path)


# =========================================================
# READ CSV
# =========================================================

try:

    df = pd.read_csv(file_path)

except Exception as e:

    print("ERROR: Could not read CSV file.")
    print(e)

    exit()


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = (
    df.columns
    .str.strip()
    .str.replace("**", "", regex=False)
    .str.replace("\\_", "_", regex=False)
)


print("\nDataset loaded successfully!")

print("Rows found:", len(df))

print("\nColumns found:")

print(df.columns.tolist())


# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [

    "State",
    "District",
    "Market",
    "Commodity",
    "Arrival_Date",
    "Modal_x0020_Price"

]


for column in required_columns:

    if column not in df.columns:

        print(
            f"\nERROR: Required column '{column}' "
            "not found in CSV."
        )

        print(
            "Available columns:",
            df.columns.tolist()
        )

        exit()


# =========================================================
# DATABASE CONNECTION
# =========================================================

db = SessionLocal()


inserted = 0
skipped = 0


# =========================================================
# IMPORT DATA
# =========================================================

for _, row in df.iterrows():

    try:

        # -------------------------------------------------
        # CROP NAME
        # -------------------------------------------------

        crop_name = str(
            row["Commodity"]
        ).strip()


        # -------------------------------------------------
        # MARKET NAME
        # -------------------------------------------------

        market_name = str(
            row["Market"]
        ).strip()


        # -------------------------------------------------
        # LOCATION
        # State + District
        # -------------------------------------------------

        state = str(
            row["State"]
        ).strip()

        district = str(
            row["District"]
        ).strip()


        location = (
            district +
            ", " +
            state
        )


        # -------------------------------------------------
        # MODAL PRICE
        # -------------------------------------------------

        price = float(
            str(
                row["Modal_x0020_Price"]
            )
            .replace(",", "")
            .replace("**", "")
            .strip()
        )


        # -------------------------------------------------
        # PRICE UNIT
        # -------------------------------------------------
        # Agmarknet prices are generally
        # reported per quintal.
        # -------------------------------------------------

        price_unit = "Quintal"


        # -------------------------------------------------
        # ARRIVAL DATE
        # -------------------------------------------------

        date = pd.to_datetime(
            row["Arrival_Date"],
            dayfirst=True,
            errors="coerce"
        )


        if pd.isna(date):

            raise ValueError(
                "Invalid arrival date"
            )


        date = date.date()


        # -------------------------------------------------
        # CREATE DATABASE OBJECT
        # -------------------------------------------------

        market_price = MarketPrice(

            crop_name=crop_name,

            market_name=market_name,

            location=location,

            price=price,

            price_unit=price_unit,

            date=date

        )


        # -------------------------------------------------
        # ADD TO DATABASE
        # -------------------------------------------------

        db.add(market_price)

        inserted += 1


    except Exception as e:

        skipped += 1


        if skipped <= 10:

            print(
                "Skipping row:",
                e
            )


# =========================================================
# SAVE DATA
# =========================================================

try:

    db.commit()

except Exception as e:

    db.rollback()

    print("\nERROR while saving data:")
    print(e)

    db.close()

    exit()


# =========================================================
# CLOSE DATABASE
# =========================================================

db.close()


# =========================================================
# RESULT
# =========================================================

print("\n================================")
print("Market data import completed!")
print("================================")

print(
    "Rows inserted:",
    inserted
)

print(
    "Rows skipped:",
    skipped
)

print("================================")

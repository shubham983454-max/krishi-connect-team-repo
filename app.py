from flask import Flask, request, jsonify, render_template

import pandas as pd
import numpy as np
import joblib


# =========================================================
# 1. CREATE FLASK APPLICATION
# =========================================================

app = Flask(__name__)


# =========================================================
# 2. LOAD TRAINED AI MODEL
# =========================================================

model = joblib.load("demand_model.pkl")


# =========================================================
# 3. LOAD DATASET
# =========================================================

df = pd.read_csv("demand_data.csv")

df["date"] = pd.to_datetime(df["date"])


# =========================================================
# 4. CROPS AVAILABLE IN OUR MARKETPLACE
# =========================================================

crops = [

    # Vegetables
    "Tomato",
    "Onion",
    "Potato",
    "Carrot",
    "Cabbage",
    "Green Chilli",
    "Brinjal",
    "Cucumber",
    "Green Peas",
    "Sweet Corn",
    "Broccoli",
    "Spinach",
    "Capsicum",
    "Beans",
    "Pumpkin",

    # Grains
    "Wheat",
    "Rice"
]


# =========================================================
# 5. MAHARASHTRA LOCATIONS
# =========================================================

locations = [

    "Pune",
    "Nashik",
    "Nagpur",
    "Mumbai",
    "Aurangabad",
    "Kolhapur",
    "Sangli",
    "Satara",
    "Ahmednagar",
    "Solapur"

]


# =========================================================
# 6. HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# 7. FORECAST API
# =========================================================

@app.route("/api/forecast")
def forecast():

    # -----------------------------------------------------
    # Get crop selected by farmer
    # -----------------------------------------------------

    crop = request.args.get(
        "crop",
        "Tomato"
    )


    # -----------------------------------------------------
    # Get location selected by farmer
    # -----------------------------------------------------

    location = request.args.get(
        "location",
        "Pune"
    )


    # -----------------------------------------------------
    # Check whether crop is valid
    # -----------------------------------------------------

    if crop not in crops:

        return jsonify({

            "error": "Invalid crop selected"

        }), 400


    # -----------------------------------------------------
    # Check whether location is valid
    # -----------------------------------------------------

    if location not in locations:

        return jsonify({

            "error": "Invalid location selected"

        }), 400


    # =====================================================
    # GET DATA FOR SELECTED CROP AND LOCATION
    # =====================================================

    selected_data = df[

        (df["crop"] == crop) &

        (df["location"] == location)

    ]


    # -----------------------------------------------------
    # Check whether data exists
    # -----------------------------------------------------

    if len(selected_data) == 0:

        return jsonify({

            "error":
            "No data available for this crop and location"

        }), 404


    # =====================================================
    # GET LATEST PRICE
    # =====================================================

    latest_price = selected_data[
        "price"
    ].iloc[-1]


    # =====================================================
    # GET LAST DATE
    # =====================================================

    last_date = df["date"].max()

    first_date = df["date"].min()


    # =====================================================
    # FORECAST NEXT 7 DAYS
    # =====================================================

    forecast_days = 7

    results = []


    for i in range(
        1,
        forecast_days + 1
    ):


        # -------------------------------------------------
        # Calculate future date
        # -------------------------------------------------

        future_date = (

            last_date +

            pd.Timedelta(
                days=i
            )

        )


        # -------------------------------------------------
        # Calculate day number
        # -------------------------------------------------

        day_number = (

            future_date -

            first_date

        ).days


        # -------------------------------------------------
        # Day of week
        # Monday = 0
        # Sunday = 6
        # -------------------------------------------------

        day_of_week = (

            future_date.dayofweek

        )


        # -------------------------------------------------
        # Month
        # -------------------------------------------------

        month = future_date.month


        # =================================================
        # CREATE INPUT FOR AI MODEL
        # =================================================

        input_data = pd.DataFrame({

            "crop": [crop],

            "location": [location],

            "day_number": [day_number],

            "day_of_week": [day_of_week],

            "month": [month],

            "price": [latest_price]

        })


        # =================================================
        # PREDICT DEMAND
        # =================================================

        prediction = model.predict(

            input_data

        )[0]


        # -------------------------------------------------
        # Prevent negative prediction
        # -------------------------------------------------

        prediction = max(

            0,

            prediction

        )


        # =================================================
        # STORE RESULT
        # =================================================

        results.append({

            "date":

                future_date.strftime(
                    "%Y-%m-%d"
                ),

            "predicted_demand":

                round(
                    prediction,
                    2
                )

        })


    # =====================================================
    # CALCULATE AVERAGE DEMAND
    # =====================================================

    average_demand = np.mean([

        item["predicted_demand"]

        for item in results

    ])


    average_demand = round(

        average_demand,

        2

    )


    # =====================================================
    # DETERMINE DEMAND LEVEL
    # =====================================================

    if average_demand >= 600:

        demand_level = "HIGH"

    elif average_demand >= 350:

        demand_level = "MEDIUM"

    else:

        demand_level = "LOW"


    # =====================================================
    # CREATE RECOMMENDATION
    # =====================================================

    if demand_level == "HIGH":

        recommendation = (

            f"Demand for {crop} in {location} "
            "is expected to be HIGH. "
            "Consider increasing supply."

        )

    elif demand_level == "MEDIUM":

        recommendation = (

            f"Demand for {crop} in {location} "
            "is expected to remain MODERATE. "
            "Maintain a balanced supply."

        )

    else:

        recommendation = (

            f"Demand for {crop} in {location} "
            "is expected to be LOW. "
            "Avoid over-supplying the market."

        )


    # =====================================================
    # SEND RESPONSE TO FRONTEND
    # =====================================================

    return jsonify({

        "crop": crop,

        "location": location,

        "average_demand":
            average_demand,

        "demand_level":
            demand_level,

        "recommendation":
            recommendation,

        "forecast":
            results

    })


# =========================================================
# 8. START FLASK SERVER
# =========================================================

if __name__ == "__main__":

    app.run(

        debug=True

    )
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error


# =========================================================
# 1. LOAD DATA
# =========================================================

print("Loading dataset...")

df = pd.read_csv("demand_data.csv")


# =========================================================
# 2. CONVERT DATE
# =========================================================

df["date"] = pd.to_datetime(df["date"])


# =========================================================
# 3. CREATE TIME FEATURES
# =========================================================

# Number of days from first date

df["day_number"] = (
    df["date"] - df["date"].min()
).dt.days


# Day of week
# Monday = 0
# Sunday = 6

df["day_of_week"] = df["date"].dt.dayofweek


# Month

df["month"] = df["date"].dt.month


# =========================================================
# 4. SELECT INPUT FEATURES
# =========================================================

features = [

    "crop",
    "location",
    "day_number",
    "day_of_week",
    "month",
    "price"

]


X = df[features]


# =========================================================
# 5. TARGET
# =========================================================

y = df["demand_kg"]


# =========================================================
# 6. SPLIT DATA
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42

)


# =========================================================
# 7. CATEGORICAL FEATURES
# =========================================================

categorical_features = [

    "crop",
    "location"

]


# =========================================================
# 8. NUMERICAL FEATURES
# =========================================================

numerical_features = [

    "day_number",
    "day_of_week",
    "month",
    "price"

]


# =========================================================
# 9. PREPROCESSING
# =========================================================

preprocessor = ColumnTransformer(

    transformers=[

        (

            "categorical",

            OneHotEncoder(
                handle_unknown="ignore"
            ),

            categorical_features

        ),

        (

            "numerical",

            "passthrough",

            numerical_features

        )

    ]

)


# =========================================================
# 10. AI MODEL
# =========================================================

model = RandomForestRegressor(

    n_estimators=100,

    max_depth=15,

    random_state=42,

    n_jobs=-1

)


# =========================================================
# 11. CREATE PIPELINE
# =========================================================

pipeline = Pipeline(

    steps=[

        (

            "preprocessor",

            preprocessor

        ),

        (

            "model",

            model

        )

    ]

)


# =========================================================
# 12. TRAIN MODEL
# =========================================================

print()

print("Training AI model...")

pipeline.fit(

    X_train,

    y_train

)


# =========================================================
# 13. MAKE TEST PREDICTIONS
# =========================================================

predictions = pipeline.predict(

    X_test

)


# =========================================================
# 14. CALCULATE ERROR
# =========================================================

mae = mean_absolute_error(

    y_test,

    predictions

)


# =========================================================
# 15. SAVE MODEL
# =========================================================

joblib.dump(

    pipeline,

    "demand_model.pkl"

)


# =========================================================
# 16. DISPLAY RESULTS
# =========================================================

print()

print("==========================================")

print("      MODEL TRAINED SUCCESSFULLY")

print("==========================================")

print()

print(
    "Training records:",
    len(X_train)
)

print(
    "Testing records:",
    len(X_test)
)

print(
    "Mean Absolute Error:",
    round(mae, 2),
    "kg"
)

print()

print(
    "Features used:"
)

for feature in features:

    print(
        " -",
        feature
    )

print()

print(
    "Model saved as: demand_model.pkl"
)

print()

print("==========================================")
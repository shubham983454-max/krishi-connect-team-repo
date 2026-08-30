
from sqlalchemy import text
from database import engine


print("================================")
print("Resetting market_prices table")
print("================================")


with engine.connect() as connection:

    # Delete old market_prices table
    connection.execute(
        text("DROP TABLE IF EXISTS market_prices")
    )

    # Create new market_prices table
    connection.execute(
        text("""
            CREATE TABLE market_prices (

                id INTEGER PRIMARY KEY,

                crop_name VARCHAR(100) NOT NULL,

                market_name VARCHAR(150) NOT NULL,

                location VARCHAR(150) NOT NULL,

                price FLOAT NOT NULL,

                price_unit VARCHAR(30) NOT NULL,

                date DATE NOT NULL

            )
        """)
    )

    connection.commit()


print("market_prices table reset successfully!")
print("================================")


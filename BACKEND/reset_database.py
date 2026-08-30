from database import SessionLocal
import models


def reset_database():

    db = SessionLocal()

    try:

        # Delete bid responses first
        deleted_responses = db.query(
            models.BidResponse
        ).delete()

        # Delete bids
        deleted_bids = db.query(
            models.Bid
        ).delete()

        # Delete crop slots
        deleted_slots = db.query(
            models.CropSlot
        ).delete()

        # Delete wholesalers
        deleted_wholesalers = db.query(
            models.Wholesaler
        ).delete()

        # Delete farmers
        deleted_farmers = db.query(
            models.Farmer
        ).delete()

        # Save changes
        db.commit()

        print()
        print("======================================")
        print("DATABASE RESET SUCCESSFUL")
        print("======================================")

        print("Bid Responses deleted :", deleted_responses)
        print("Bids deleted          :", deleted_bids)
        print("Crop Slots deleted    :", deleted_slots)
        print("Wholesalers deleted   :", deleted_wholesalers)
        print("Farmers deleted       :", deleted_farmers)

        print()
        print("Market Prices         : NOT DELETED")
        print("======================================")

    except Exception as error:

        db.rollback()

        print()
        print("DATABASE RESET FAILED")
        print("ERROR:", error)

    finally:

        db.close()


if __name__ == "__main__":
    reset_database()
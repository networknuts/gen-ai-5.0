from fastapi import FastAPI, HTTPException
from datetime import date, timedelta

app = FastAPI()

# -----------------------------
# FAKE DATABASE
# -----------------------------
fake_orders = {
    1: {
        "user_id": 1,
        "item": "Laptop",
        "delivery_date": date.today() + timedelta(days=2),
        "status": "Out for delivery"
    },
    2: {
        "user_id": 2,
        "item": "Headphones",
        "delivery_date": date.today() + timedelta(days=5),
        "status": "Shipped"
    },
    3: {
        "user_id": 3,
        "item": "Book",
        "delivery_date": date.today() + timedelta(days=1),
        "status": "Arriving tomorrow"
    }
}

# -----------------------------
# API ENDPOINT
# -----------------------------
@app.get("/delivery/{user_id}")
def get_delivery(user_id: int):
    if user_id not in fake_orders:
        raise HTTPException(status_code=404, detail="User not found")

    return fake_orders[user_id]

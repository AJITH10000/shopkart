import os
import json
import redis
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

app = FastAPI(title="Cart Service", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(REDIS_URL, decode_responses=True)
CART_TTL = 60 * 60 * 24 * 7  # 7 days

class CartItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int
    image_url: Optional[str] = None

class CartItemAdd(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int = 1
    image_url: Optional[str] = None

class CartResponse(BaseModel):
    user_id: str
    items: List[CartItem]
    total: float
    item_count: int

def cart_key(user_id: str) -> str:
    return f"cart:{user_id}"

def get_cart_data(user_id: str) -> List[dict]:
    data = r.get(cart_key(user_id))
    return json.loads(data) if data else []

def save_cart(user_id: str, items: List[dict]):
    r.setex(cart_key(user_id), CART_TTL, json.dumps(items))

@app.get("/health")
def health():
    return {"status": "ok", "service": "cart-service"}

@app.get("/cart/{user_id}", response_model=CartResponse)
def get_cart(user_id: str):
    items = get_cart_data(user_id)
    total = sum(i["price"] * i["quantity"] for i in items)
    return {"user_id": user_id, "items": items, "total": round(total, 2), "item_count": len(items)}

@app.post("/cart/{user_id}/items", response_model=CartResponse)
def add_item(user_id: str, item: CartItemAdd):
    items = get_cart_data(user_id)
    for existing in items:
        if existing["product_id"] == item.product_id:
            existing["quantity"] += item.quantity
            save_cart(user_id, items)
            return get_cart(user_id)
    items.append(item.dict())
    save_cart(user_id, items)
    return get_cart(user_id)

@app.put("/cart/{user_id}/items/{product_id}")
def update_item(user_id: str, product_id: str, quantity: int):
    items = get_cart_data(user_id)
    if quantity <= 0:
        items = [i for i in items if i["product_id"] != product_id]
    else:
        for item in items:
            if item["product_id"] == product_id:
                item["quantity"] = quantity
                break
        else:
            raise HTTPException(status_code=404, detail="Item not in cart")
    save_cart(user_id, items)
    return get_cart(user_id)

@app.delete("/cart/{user_id}/items/{product_id}", status_code=204)
def remove_item(user_id: str, product_id: str):
    items = get_cart_data(user_id)
    items = [i for i in items if i["product_id"] != product_id]
    save_cart(user_id, items)

@app.delete("/cart/{user_id}", status_code=204)
def clear_cart(user_id: str):
    r.delete(cart_key(user_id))

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.core.database import get_db
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate

router = APIRouter()

@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    total = sum(item.price * item.quantity for item in payload.items)
    order = Order(
        user_id=payload.user_id,
        total_amount=round(total, 2),
        shipping_address=payload.shipping_address,
        notes=payload.notes,
    )
    db.add(order)
    db.flush()
    for item in payload.items:
        db.add(OrderItem(order_id=order.id, **item.dict()))
    db.commit()
    db.refresh(order)
    return order

@router.get("/", response_model=List[OrderResponse])
def list_orders(user_id: UUID = None, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    q = db.query(Order)
    if user_id:
        q = q.filter(Order.user_id == user_id)
    return q.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: UUID, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_status(order_id: UUID, payload: OrderStatusUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.status = payload.status
    if payload.payment_id:
        order.payment_id = payload.payment_id
    db.commit()
    db.refresh(order)
    return order

@router.delete("/{order_id}", status_code=204)
def cancel_order(order_id: UUID, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status not in [OrderStatus.PENDING, OrderStatus.CONFIRMED]:
        raise HTTPException(status_code=400, detail="Cannot cancel order in current status")
    order.status = OrderStatus.CANCELLED
    db.commit()

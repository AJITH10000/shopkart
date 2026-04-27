import uuid
import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from app.core.database import get_db
from app.models.payment import Payment, PaymentStatus
from app.schemas.payment import PaymentCreate, PaymentResponse

router = APIRouter()

def mock_process_payment(amount: float, method: str) -> dict:
    """Simulate payment gateway — 90% success rate"""
    success = random.random() > 0.1
    if success:
        return {"success": True, "transaction_id": f"TXN-{uuid.uuid4().hex[:12].upper()}"}
    return {"success": False, "reason": "Payment gateway declined"}

@router.post("/", response_model=PaymentResponse, status_code=201)
def initiate_payment(payload: PaymentCreate, db: Session = Depends(get_db)):
    payment = Payment(
        order_id=payload.order_id,
        user_id=payload.user_id,
        amount=payload.amount,
        currency=payload.currency,
        method=payload.method,
        status=PaymentStatus.PENDING,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    result = mock_process_payment(payload.amount, payload.method)
    if result["success"]:
        payment.status = PaymentStatus.SUCCESS
        payment.transaction_id = result["transaction_id"]
    else:
        payment.status = PaymentStatus.FAILED
        payment.failure_reason = result["reason"]

    db.commit()
    db.refresh(payment)
    return payment

@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: UUID, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.get("/order/{order_id}", response_model=List[PaymentResponse])
def get_payments_by_order(order_id: UUID, db: Session = Depends(get_db)):
    return db.query(Payment).filter(Payment.order_id == order_id).all()

@router.post("/{payment_id}/refund", response_model=PaymentResponse)
def refund_payment(payment_id: UUID, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if payment.status != PaymentStatus.SUCCESS:
        raise HTTPException(status_code=400, detail="Only successful payments can be refunded")
    payment.status = PaymentStatus.REFUNDED
    db.commit()
    db.refresh(payment)
    return payment

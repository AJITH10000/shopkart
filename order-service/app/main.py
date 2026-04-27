from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import orders
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(orders.router, prefix="/orders", tags=["orders"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "order-service"}

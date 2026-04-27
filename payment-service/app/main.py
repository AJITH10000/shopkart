from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import payments
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Payment Service", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "payment-service"}

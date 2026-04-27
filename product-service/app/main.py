from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import products, categories
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Service", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "product-service"}

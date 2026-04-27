# ShopKart — Microservices E-Commerce Platform

A production-grade e-commerce backend built with Python (FastAPI), containerized with Docker, and deployed on AWS EKS.

## Architecture

| Service | Port | Database | Description |
|---|---|---|---|
| user-service | 8000 | PostgreSQL | Auth, registration, profile |
| product-service | 8001 | PostgreSQL | Products, categories, stock |
| cart-service | 8002 | Redis | Cart management (session-based) |
| order-service | 8003 | PostgreSQL | Order lifecycle management |
| payment-service | 8004 | PostgreSQL | Payment processing (mock gateway) |

## Project Structure

```
shopkart/
├── user-service/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/         # database.py, security.py
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── routers/      # FastAPI routers
│   ├── Dockerfile
│   └── requirements.txt
├── product-service/      # same structure
├── cart-service/         # Redis-based, single main.py
├── order-service/        # same structure
├── payment-service/      # same structure
├── docker-compose.yml    # local dev
└── init-db.sql           # creates all databases
```

## Quick Start (Local)

### Prerequisites
- Docker & Docker Compose installed

### Run all services
```bash
git clone <your-repo-url>
cd shopkart
docker compose up --build
```

### Verify all services are healthy
```bash
curl http://localhost:8000/health   # user-service
curl http://localhost:8001/health   # product-service
curl http://localhost:8002/health   # cart-service
curl http://localhost:8003/health   # order-service
curl http://localhost:8004/health   # payment-service
```

### API Docs (Swagger UI)
- User Service:    http://localhost:8000/docs
- Product Service: http://localhost:8001/docs
- Cart Service:    http://localhost:8002/docs
- Order Service:   http://localhost:8003/docs
- Payment Service: http://localhost:8004/docs

## Sample API Flow

### 1. Register a user
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@shopkart.com","full_name":"Test User","password":"pass1234"}'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@shopkart.com","password":"pass1234"}'
```

### 3. Create a product
```bash
curl -X POST http://localhost:8001/products \
  -H "Content-Type: application/json" \
  -d '{"name":"iPhone 15","price":79999,"stock":50,"sku":"APPL-IP15-001"}'
```

### 4. Add to cart
```bash
curl -X POST http://localhost:8002/cart/<user_id>/items \
  -H "Content-Type: application/json" \
  -d '{"product_id":"<product_id>","name":"iPhone 15","price":79999,"quantity":1}'
```

### 5. Place order
```bash
curl -X POST http://localhost:8003/orders \
  -H "Content-Type: application/json" \
  -d '{
    "user_id":"<user_id>",
    "items":[{"product_id":"<product_id>","product_name":"iPhone 15","price":79999,"quantity":1}],
    "shipping_address":{"street":"123 MG Road","city":"Bengaluru","pincode":"560001"}
  }'
```

### 6. Make payment
```bash
curl -X POST http://localhost:8004/payments \
  -H "Content-Type: application/json" \
  -d '{"order_id":"<order_id>","user_id":"<user_id>","amount":79999,"method":"card"}'
```

## Environment Variables

| Variable | Service | Default | Description |
|---|---|---|---|
| DATABASE_URL | all except cart | postgresql://... | PostgreSQL connection |
| REDIS_URL | cart | redis://localhost:6379 | Redis connection |
| SECRET_KEY | user | shopkart-secret | JWT signing key |


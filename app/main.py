from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

# Database configuration
DATABASE_URL = os.environ["DATABASE_URL"]

print(f"Connecting to database at {DATABASE_URL}")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Initialize FastAPI app
app = FastAPI(title="Order Management API", version="1.0.0")


# Database Models
class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)


# Pydantic Models
class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=100)
    product_name: str = Field(..., min_length=1, max_length=200)
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    status: Optional[str] = Field(
        default="pending", pattern="^(pending|processing|completed|cancelled)$"
    )


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    product_name: str
    quantity: int
    price: float
    status: str
    created_at: datetime
    total_amount: float

    class Config:
        from_attributes = True

    @staticmethod
    def from_orm(order: OrderModel) -> "OrderResponse":
        return OrderResponse(
            id=order.id,
            customer_name=order.customer_name,
            product_name=order.product_name,
            quantity=order.quantity,
            price=order.price,
            status=order.status,
            created_at=order.created_at,
            total_amount=order.quantity * order.price,
        )


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    database: str


# Create tables
Base.metadata.create_all(bind=engine)


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Routes
@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "Order Management API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "create_order": "POST /orders",
            "list_orders": "GET /orders",
        },
    }


@app.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint to verify API and database connectivity
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return HealthResponse(
        status="healthy" if db_status == "connected" else "unhealthy",
        timestamp=datetime.now(),
        database=db_status,
    )


@app.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order
    """
    try:
        # Create new order instance
        db_order = OrderModel(
            customer_name=order.customer_name,
            product_name=order.product_name,
            quantity=order.quantity,
            price=order.price,
            status=order.status,
        )

        # Add to database
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        return OrderResponse.from_orm(db_order)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/orders", response_model=List[OrderResponse])
async def list_orders(status: Optional[str] =
                      None, db: Session = Depends(get_db)):
    """
    List all orders with optional status filter
    """
    try:
        query = db.query(OrderModel)

        # Apply status filter if provided
        if status:
            query = query.filter(OrderModel.status == status)

        # Order by creation date (newest first)
        orders = query.order_by(OrderModel.created_at.desc()).all()

        return [OrderResponse.from_orm(order) for order in orders]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    Get a specific order by ID
    """
    order = db.query(OrderModel).filter(OrderModel.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return OrderResponse.from_orm(order)


# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

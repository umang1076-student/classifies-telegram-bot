from pydantic import BaseModel
from datetime import datetime


# Schema for creating an ad (request body)
class AdCreate(BaseModel):
    title: str
    price: float
    description: str
    category: str
    contact: str


# Schema for returning an ad (response)
class AdResponse(AdCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # This allows SQLAlchemy model to convert to dict
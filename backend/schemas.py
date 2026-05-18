from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ListingCreate(BaseModel):
    business_name: str
    category: str
    city: str
    address: Optional[str] = None
    phone: Optional[str] = None
    source: str

class ListingOut(ListingCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
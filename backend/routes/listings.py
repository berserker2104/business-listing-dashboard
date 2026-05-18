from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Listing
from schemas import ListingCreate
from typing import List

router = APIRouter(prefix="/listings", tags=["Listings"])

@router.post("/bulk-insert")
def bulk_insert(listings: List[ListingCreate], db: Session = Depends(get_db)):
    objects = [Listing(**l.dict()) for l in listings]
    db.add_all(objects)
    db.commit()
    return {"message": f"{len(objects)} listings inserted successfully"}

@router.get("/all")
def get_all(db: Session = Depends(get_db)):
    return db.query(Listing).limit(100).all()
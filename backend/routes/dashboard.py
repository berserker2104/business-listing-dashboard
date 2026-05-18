from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Listing

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/city-wise")
def city_wise(db: Session = Depends(get_db)):
    results = db.query(Listing.city, func.count(Listing.id).label("count"))\
                .group_by(Listing.city).all()
    return [{"city": r.city, "count": r.count} for r in results]

@router.get("/category-wise")
def category_wise(db: Session = Depends(get_db)):
    results = db.query(Listing.category, func.count(Listing.id).label("count"))\
                .group_by(Listing.category).all()
    return [{"category": r.category, "count": r.count} for r in results]

@router.get("/source-wise")
def source_wise(db: Session = Depends(get_db)):
    results = db.query(Listing.source, func.count(Listing.id).label("count"))\
                .group_by(Listing.source).all()
    return [{"source": r.source, "count": r.count} for r in results]

@router.get("/summary")
def summary(db: Session = Depends(get_db)):
    total = db.query(func.count(Listing.id)).scalar()
    cities = db.query(func.count(func.distinct(Listing.city))).scalar()
    categories = db.query(func.count(func.distinct(Listing.category))).scalar()
    return {"total_listings": total, "total_cities": cities, "total_categories": categories}
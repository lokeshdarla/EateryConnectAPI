from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from typing import List

from ..database import get_db
from .. import schemas, models

router = APIRouter(
    prefix="/cuisines",
    tags=["Customers"]
)

# Get all cuisines
@router.get("/")
def get_all_cuisines(db: Session = Depends(get_db)):
    cuisines_query = db.query(models.Cuisine).join(models.Restaurant, models.Restaurant.restaurant_id == models.Cuisine.restaurant_id)
    print(str(cuisines_query))
    cuisines = cuisines_query.all()
    return cuisines




# Get cuisine by ID
@router.get("/{id}")
def get_cuisine_by_id(id: str, db: Session = Depends(get_db)):
    cuisine = db.query(models.Cuisine).filter(models.Cuisine.menu_id == id).first()
    if cuisine:
        return cuisine
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuisine not found")


# Create a new cuisine
@router.post("/", response_model=schemas.CuisineBase)
def create_cuisine(cuisine_data: schemas.CuisineCreate, db: Session = Depends(get_db)):
    new_cuisine = models.Cuisine(**cuisine_data.dict())
    db.add(new_cuisine)
    db.commit()
    db.refresh(new_cuisine)
    return new_cuisine


# Update cuisine by ID
@router.put("/{id}", response_model=schemas.CuisineBase)
def update_cuisine(id: str, cuisine_data: schemas.CuisineUpdate, db: Session = Depends(get_db)):
    existing_cuisine = db.query(models.Cuisine).filter(models.Cuisine.menu_id == id).first()
    if not existing_cuisine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuisine not found")

    for key, value in cuisine_data.dict(exclude_unset=True).items():
        setattr(existing_cuisine, key, value)

    db.commit()
    db.refresh(existing_cuisine)
    return existing_cuisine


# Delete cuisine by ID
@router.delete("/{id}", response_model=schemas.CuisineBase)
def delete_cuisine(id: str, db: Session = Depends(get_db)):
    cuisine = db.query(models.Cuisine).filter(models.Cuisine.menu_id == id).first()
    if not cuisine:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cuisine not found")

    db.delete(cuisine)
    db.commit()

    return cuisine

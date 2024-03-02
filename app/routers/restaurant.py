from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, models

router = APIRouter(
    prefix="/restaurants",
    tags=["Customers"]
)

# Get all restaurants
@router.get("/", response_model=list[schemas.RestaurantOut], status_code=status.HTTP_200_OK)
def get_all_restaurants(db: Session = Depends(get_db)):
    restaurants = db.query(models.Restaurant).all()

    if not restaurants:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No restaurants found")

    return restaurants


# Get restaurant by ID
@router.get("/{id}", response_model=schemas.RestaurantBase, status_code=status.HTTP_200_OK)
def get_restaurant_by_id(id: str, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.restaurant_id == id).first()

    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

    return restaurant


# Create a new restaurant
@router.post("/", response_model=schemas.RestaurantBase, status_code=status.HTTP_201_CREATED)
def create_restaurant(restaurant_data: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    new_restaurant = models.Restaurant(**restaurant_data.dict())
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    return new_restaurant


# Update restaurant by ID
@router.put("/{id}", response_model=schemas.RestaurantBase, status_code=status.HTTP_200_OK)
def update_restaurant(id: str, restaurant_data: schemas.RestaurantUpdate, db: Session = Depends(get_db)):
    existing_restaurant = db.query(models.Restaurant).filter(models.Restaurant.restaurant_id == id).first()

    if not existing_restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

    for key, value in restaurant_data.dict(exclude_unset=True).items():
        setattr(existing_restaurant, key, value)

    db.commit()
    db.refresh(existing_restaurant)
    return existing_restaurant


# Delete restaurant by ID
@router.delete("/{id}", response_model=schemas.RestaurantBase, status_code=status.HTTP_200_OK)
def delete_restaurant(id: str, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.restaurant_id == id).first()

    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")

    db.delete(restaurant)
    db.commit()

    return restaurant

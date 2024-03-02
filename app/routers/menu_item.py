from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.orm import joinedload
from ..database import get_db
from ..import schemas,models

router = APIRouter(
    prefix="/menu-items",
    tags=["Menu"]
)

@router.get("/", response_model=List[schemas.MenuItemOut])
def get_all_menu_items(db: Session = Depends(get_db)):
    items = (
        db.query(models.MenuItem)
        .join(models.MenuItem.cuisine)
        .join(models.Cuisine.restaurant)
        .all()
    )

    result = [
        schemas.MenuItemOut(
            menu_id=str(item.menu_id),
            item_name=item.item_name,
            price=item.price,
            cuisine=schemas.CuisineOut(
                cuisine_name=item.cuisine.cuisine_name,  # Fixed typo in attribute name
                restaurant=schemas.RestaurantOut(  # Added missing parentheses
                    name=item.cuisine.restaurant.name,
                    address=item.cuisine.restaurant.address,
                    phone=item.cuisine.restaurant.phone
                )
            )
        )
        for item in items
    ]

    return result


#Create a new food item
@router.post("/",response_model=schemas.MenuItemBase)
def create_menu_item(menu_data:schemas.MenuItemCreate,db:Session=Depends(get_db)):
  new_item=models.MenuItem(**menu_data.dict())
  db.add(new_item)
  db.commit()
  db.refresh(new_item)
  return new_item

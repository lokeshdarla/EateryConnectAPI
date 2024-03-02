from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import schemas, models

router = APIRouter(
   tags=["Customers"]
)

@router.post("/drivers/", response_model=schemas.DriverResponse, status_code=status.HTTP_201_CREATED)
def create_driver(driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    db_driver = models.Driver(**driver.dict())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    db_driver.driver_id=str(db_driver.driver_id)
    return db_driver
  
@router.get("/drivers/", response_model=List[schemas.DriverResponse])
def get_all_drivers(db: Session = Depends(get_db)):
    drivers = db.query(models.Driver).all()
    for driver in drivers:
        driver.driver_id = str(driver.driver_id)
    return drivers or []
  
@router.get("/drivers/{driver_id}", response_model=schemas.DriverResponse)
def read_driver(driver_id: str, db: Session = Depends(get_db)):
    driver = db.query(models.Driver).filter(models.Driver.driver_id == driver_id).first()
    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")
    driver.driver_id = str(driver.driver_id)
    return driver

@router.put("/drivers/{driver_id}", response_model=schemas.DriverResponse)
def update_driver(driver_id: str, driver: schemas.DriverCreate, db: Session = Depends(get_db)):
    db_driver = db.query(models.Driver).filter(models.Driver.driver_id == driver_id).first()
    if db_driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")

    for key, value in driver.dict().items():
        setattr(db_driver, key, value)

    db.commit()
    db.refresh(db_driver)
    db_driver.driver_id=str(db_driver.driver_id)
    return db_driver

@router.delete("/drivers/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_driver(driver_id: str, db: Session = Depends(get_db)):
    db_driver = db.query(models.Driver).filter(models.Driver.driver_id == driver_id).first()
    if db_driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")

    db.delete(db_driver)
    db.commit()

    return {"detail": "Driver successfully deleted"}


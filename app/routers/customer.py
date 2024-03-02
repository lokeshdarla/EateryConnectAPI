from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import schemas, models, utils

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

@router.get("/",response_model=List[schemas.CustomerOut])
def get_all_customers(db: Session = Depends(get_db)):
    customers = db.query(models.User).all()
    return customers or []

@router.get("/{id}", response_model=schemas.CustomerOut)
def get_customer_by_id(id: str, db: Session = Depends(get_db)):
    customer = db.query(models.User).filter(models.User.user_id == id).first()
    if customer:
        return customer
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found with the given id")

@router.post("/", response_model=schemas.CustomerOut)
def add_customer(customer: schemas.CustomerBase, db: Session = Depends(get_db)):
    customer.password = utils.hash(password=customer.password)
    new_customer = models.User(**customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return schemas.CustomerOut(
        name=new_customer.name,
        phone=new_customer.phone,
        email=new_customer.email,
        created_at=new_customer.created_at
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(id: str, db: Session = Depends(get_db)):
    customer = db.query(models.User).filter(models.User.user_id == id).first()
    if customer:
        db.delete(customer)
        db.commit()
        return {"detail": "Account Deleted Successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found with the given id")

@router.put("/{id}", response_model=schemas.CustomerOut)
def update_customer(id: str, new_customer: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.query(models.User).filter(models.User.user_id == id).first()
    if customer:
        for field, value in new_customer.dict().items():
            setattr(customer, field, value)
        db.commit()
        db.refresh(customer)
        return customer
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found with the given id")

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...db.base import get_db
from ..schemas import customer 
from ...db.models.customer import Customer
from ...utils import helpers
from ...core import oauth2

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

@router.get("/", response_model=List[customer.CustomerOut])
def get_all_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return customers or []

@router.get("/{id}", response_model=customer.CustomerOut)
def get_customer_by_id(id: str, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.id == id).first()
    if db_customer:
        return db_customer
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found with the given id")

@router.post("/", response_model=customer.CustomerOut, status_code=status.HTTP_201_CREATED)
def add_customer(new_customer: customer.CustomerBase, db: Session = Depends(get_db)):
    new_customer.password = helpers.hash(password=new_customer.password)
    new_customer = Customer(**new_customer.dict())
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return customer.CustomerOut(
        id=new_customer.id,
        name=new_customer.name,
        phone=new_customer.phone,
        email=new_customer.email,
        created_at=new_customer.created_at
    )

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    db_customer = db.query(Customer).filter(current_user['id'] == Customer.id).first()
    if db_customer:
        db.delete(db_customer)
        db.commit()
        return {"detail": "Account Deleted Successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found with the given id")

@router.put("/", response_model=customer.CustomerOut)
def update_customer(new_customer: customer.CustomerUpdate, db: Session = Depends(get_db), current_user: dict = Depends(oauth2.get_current_user)):
    db_customer = db.query(Customer).filter(Customer.id == current_user['id']).first()
    if db_customer:
        for field, value in new_customer.dict().items():
            setattr(db_customer, field, value)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found with the given id")

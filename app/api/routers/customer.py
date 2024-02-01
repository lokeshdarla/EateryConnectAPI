from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...db.base import get_db
from ..schemas import customer 
from ...db.models.customer import Customer
from ...utils import helpers

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

@router.get("/",response_model=List[customer.CustomerOut])
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

@router.post("/", response_model=customer.CustomerOut)
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(id: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == id).first()
    if customer:
        db.delete(customer)
        db.commit()
        return {"detail": "Account Deleted Successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found with the given id")

@router.put("/{id}", response_model=customer.CustomerOut)
def update_customer(id: str, new_customer: customer.CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == id).first()
    if customer:
        for field, value in new_customer.dict().items():
            setattr(customer, field, value)
        db.commit()
        db.refresh(customer)
        return customer
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found with the given id")

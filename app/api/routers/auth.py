from fastapi import APIRouter,HTTPException,Depends,status
from ...utils import helpers
from ...core import oauth2
from sqlalchemy.orm import Session
from ..schemas import token,customer
from ...db.base import get_db
from ...db.models.customer import Customer
router =APIRouter(tags=["Authentication"])

@router.post("/login", response_model=token.Token)
def login(customer_cred: customer.CustomerLogin, db: Session = Depends(get_db)):
    db_customer = db.query(Customer).filter(Customer.email == customer_cred.email).first()
    
    if not db_customer:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    
    if not helpers.verify(customer_cred.password, db_customer.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": db_customer.id, "name": db_customer.name, "email": db_customer.email})
    return {"access_token": access_token}


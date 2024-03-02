from fastapi import APIRouter,HTTPException,Depends,status
from ..import models,schemas,oauth2,utils
from sqlalchemy.orm import Session
from ..database import get_db

router =APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(customer_cred: schemas.CustomerLogin, db: Session = Depends(get_db)):
    customer = db.query(models.User).filter(models.User.email == customer_cred.email).first()
    
    if not customer:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    
    if not utils.verify(customer_cred.password, customer.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

    user_id_str = str(customer.user_id)
    access_token = oauth2.create_access_token(data={"user_id": user_id_str, "name": customer.name, "email": customer.email})
    return {"access_token": access_token}


from jose import JWTError
import jwt
from datetime import datetime, timedelta
from fastapi import status, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from . import database, schemas, models
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

# Function to create an access token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(hours=settings.ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
  
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
        user_name = payload.get("customer_name")
        user_email = payload.get("customer_email")

        if user_id is None:
            raise credentials_exception

        # Convert UUID to string
        user_id_str = str(user_id)

        token_data = {"user_id": user_id_str, "customer_name": user_name, "customer_email": user_email}
        return token_data
    except JWTError as e:
        raise credentials_exception

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)
    
    # Query the database using the string representation of UUID
    user = db.query(models.User).filter(models.User.id == token_data["user_id"]).first()
    return user

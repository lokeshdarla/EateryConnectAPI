from pydantic import BaseModel
from datetime import datetime


class CustomerBase(BaseModel):
  name:str
  phone:str
  email:str
  password:str

class CustomerLogin(BaseModel):
  email:str
  password:str

class CustomerOut(BaseModel):
  id:int
  name:str
  phone:str
  email:str
  created_at:datetime

class CustomerUpdate(BaseModel):
  name:str
  phone:str
  email:str
  
class CustomerPassowordChange(BaseModel):
  email:str
  phone:str
  password:str

class CustomerLogin(BaseModel):
    email: str
    password: str

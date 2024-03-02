from pydantic import BaseModel,UUID4
from typing import Optional
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

class Token(BaseModel):
    access_token: str


class RestaurantBase(BaseModel):
    name: str
    address: str
    phone: str

class RestaurantCreate(BaseModel):
    name: str
    address: str
    phone: str
    
class RestaurantUpdate(RestaurantBase):
    pass

class RestaurantOut(RestaurantBase):
    restaurant_id:UUID4

class CuisineBase(BaseModel):
    cuisine_name: str
    restaurant_id: str

class CuisineCreate(BaseModel):
    cuisine_name: str
    restaurant_id: str

class CuisineUpdate(BaseModel):
    cuisine_name: str

class CuisineOut(BaseModel):
   cuisine_name: str
   restaurant:RestaurantBase

# MenuItemSchema
class MenuItemBase(BaseModel):
    menu_id:UUID4
    item_name:str
    price:float
    is_available:bool=True

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemUpdate(MenuItemBase):
    pass

class MenuItemOut(BaseModel):
   menu_id:str
   item_name:str
   price:float
   cuisine:CuisineOut


class DriverCreate(BaseModel):
    name: str
    phone: str
    email: str
    location: str = "immobile"

class DriverResponse(BaseModel):
    driver_id: str
    name: str
    phone: str
    email: str
    location: str

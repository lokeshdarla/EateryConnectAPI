from sqlalchemy import Column, String, Boolean, Integer, TIMESTAMP, text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

class User(Base):
    __tablename__ = "users"
  
    user_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))

class Restaurant(Base):
    __tablename__ = "restaurants"
  
    restaurant_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    name = Column(String, nullable=False, unique=True)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    # Define a relationship to the Cuisine model
    cuisines = relationship("Cuisine", back_populates="restaurant")

class Order(Base):
    __tablename__ = "orders"
  
    order_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey('restaurants.restaurant_id'))
    order_total = Column(DECIMAL, nullable=True)
    delivery_status = Column(String, nullable=False)
    driver_name = Column(String, nullable=False, server_default=text('Not assigned'))
    driver_phone = Column(String, nullable=False, server_default=text('Not Available'))

    payments = relationship('Payment', back_populates='order')  # Add this line

class Payment(Base):
    __tablename__ = "payments"
  
    payment_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.order_id'), nullable=False)
    payment_method = Column(String(20), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(20), nullable=False)
  
    order = relationship('Order', back_populates='payments')

  
class Driver(Base):
    __tablename__ = "drivers"
  
    driver_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    location = Column(String, nullable=False)


class Rating(Base):
    __tablename__ = "ratings"
  
    rating_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.restaurant_id"))
    rating = Column(Integer, nullable=False)

class Address(Base):
    __tablename__ = "addresses"
  
    address_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    state = Column(String, nullable=False)
    city = Column(String, nullable=False)
    street = Column(String, nullable=False)
    pincode = Column(String, nullable=False)

class Cuisine(Base):
    __tablename__ = "cuisines"
  
    menu_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    cuisine_name = Column(String, nullable=False, unique=True)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.restaurant_id"))

    # Define a relationship to the Restaurant model
    restaurant = relationship("Restaurant", back_populates="cuisines")
    menu_items = relationship("MenuItem", back_populates="cuisine")


class MenuItem(Base):
    __tablename__ = "menu_items"
  
    menu_item_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()'))
    menu_id = Column(UUID(as_uuid=True), ForeignKey("cuisines.menu_id"))
    item_name = Column(String, nullable=False)
    price = Column(DECIMAL, nullable=False)
    is_available =Column(Boolean,server_default='True',nullable=False)

    cuisine = relationship("Cuisine", back_populates="menu_items")
  

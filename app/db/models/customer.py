from sqlalchemy import Column, String, Integer, TIMESTAMP, text
from ..base import Base

class Customer(Base):
    __tablename__ = "customers"
  
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('now()'))
    
    def to_dict(self):
      return{
        "id":self.id,
        "name":self.name,
        "email":self.email,
        "password":self.password,
        "phone":self.phone,
        "created_at": self.created_at.isoformat() 
      }

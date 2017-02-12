from sqlalchemy import Column,Integer,String, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
from passlib.apps import custom_app_context as pwd_context


Base = declarative_base()

class Horse(Base):
    __tablename__ = 'horse'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    photo = Column(String)
    price = Column(String)
    carts= relationship("CartAssociation", back_populates="horse")
class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}  #This will enable us to add more columns later
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address= Column(String)
    email = Column(String)
    password_hash= Column(String)
    cart = relationship("Cart", uselist=False, back_populates="user")
    def hash_password(self, password):
        self.password_hash=pwd_context.encrypt(password)
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)
    
class Cart(Base):
    __tablename__ = 'cart'
    __table_args__ = {'extend_existing': True}  #This will enable us to add more columns later
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="cart")
    horses = relationship("CartAssociation", back_populates="cart")

class CartAssociation(Base):
    __tablename__ = 'CartAssociation'
    cart_id = Column(Integer, ForeignKey('cart.id'), primary_key=True)
    horse_id = Column(Integer, ForeignKey('horse.id'), primary_key=True)
    horse = relationship("Horse", back_populates="carts")
    cart = relationship("Cart", back_populates="horses")

 
engine = create_engine('sqlite:///my_horse.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()


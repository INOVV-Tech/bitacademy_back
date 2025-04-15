from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy import Column, UUID, Integer, String, ForeignKey, TIMESTAMP, Enum, Boolean, ARRAY

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'test'}

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

class AddressModel(Base):
    __tablename__ = 'addresses'
    __table_args__ = {'schema': 'test'}

    id = Column(Integer, primary_key=True)
    street = Column(String)
    number = Column(String)
    city = Column(String)
    state = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))

class FreeResourceModel(Base):
    __tablename__ = 'free_resources'
    __table_args__ = { 'schema': 'test' }

    id = Column(Integer, primary_key=True)
    title = Column(String)
    created_at = Column(TIMESTAMP(timezone=True))
    url = Column(String)
    tags = Column(ARRAY(String))
"""This file contains Employee model"""

from sqlalchemy import Column, String
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from .database import Base

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(GUID, primary_key= True, default=GUID_DEFAULT_SQLITE)
    name = Column(String, nullable= False)
    department = Column(String, nullable= False)

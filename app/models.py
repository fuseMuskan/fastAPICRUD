from .database import Base
from sqlalchemy import Column, String, Boolean
from sqlalchemy.sql import func
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(GUID, primary_key= True, default=GUID_DEFAULT_SQLITE)
    name = Column(String, nullable= False)
    department = Column(String, nullable= False)



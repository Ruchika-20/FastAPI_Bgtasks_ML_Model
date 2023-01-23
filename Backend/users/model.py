from Backend.database.database import Base
from sqlalchemy import Column,String,Integer
from Backend.utils.util import Common

class UserModel(Base,Common):

    __tablename__ = "user"
    user_name=Column(String,nullable=False)
    
    
    
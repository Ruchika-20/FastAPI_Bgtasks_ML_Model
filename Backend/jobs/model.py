from Backend.database.database import Base
from sqlalchemy import String,Column,ForeignKey,Float
from Backend.utils.util import Common
from Backend.users.model import UserModel
from sqlalchemy.dialects.postgresql import UUID

class JobModel(Base,Common):
    __tablename__="job"
    job_name = Column(String,nullable=False)        #name of the model used for training
    created_by = Column(UUID,ForeignKey(UserModel.id))
    updated_by = Column(UUID)
    input_features = Column(String,nullable=False)
    output_features = Column(String,nullable=False)
    algorithm = Column(String,nullable=False)
    accuracy=Column(Float,default=0)
    estimated_time=Column(Float,default=0)
    download=Column(String)


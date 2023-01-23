from Backend.database.database import Base
from sqlalchemy import Column,ForeignKey,String
from Backend.utils.util import Common
from Backend.jobs.model import JobModel
from sqlalchemy.dialects.postgresql import UUID

class FileModel(Base,Common):
    
    __tablename__ = "file"
    file_name=Column(String,nullable=False)
    job_id = Column(UUID,ForeignKey(JobModel.id))


    

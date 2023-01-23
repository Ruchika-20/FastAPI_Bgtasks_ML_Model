from pydantic import BaseModel

class FilesSchema(BaseModel):
    
    file_name:str
    job_id:str
    
    
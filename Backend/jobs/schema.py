from pydantic import BaseModel

class JobSchema(BaseModel):
    
    job_name:str
    input_features: str
    output_features: str
    algorithm: str
    created_by:str
    
    
    class Config:
        schema_extra = {
            "example": {
                "job_name":"mlmodel",
                "input_features": "sepal_length,sepal_width,petal_length,petal_width",
                "output_features": "species",
                "algorithm": "classification",
                "created_by": "xyz",
            }
        }

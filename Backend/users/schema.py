from pydantic import BaseModel

class UserSchema(BaseModel):
    user_name: str
    
    class Config:
        orm_mode = True

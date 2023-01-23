from fastapi import APIRouter,Depends
from Backend.users.model import UserModel
from Backend.jobs.model import JobModel
from Backend.users.schema import UserSchema
from sqlalchemy.orm import Session
from Backend.database.database import get_db

user = APIRouter()

def common_query(db,user_id):
    return db.query(UserModel).filter(UserModel.id == user_id)

def common_filter(db,user_id):
    return db.query(JobModel).filter(JobModel.created_by==user_id)

#CREATING THE USER
@user.post("/userpost")
def create_user(user: UserSchema,db: Session = Depends(get_db)):
    
    new_user = UserModel(user_name=user.user_name)
    db.add(new_user)
    db.commit()
    return {"status": 200, "message": "User added successfully"}

#READING THE USER
@user.get("/user")
def read_all_users(db: Session = Depends(get_db)):

    user = db.query(UserModel).all()
    return {"data": user, "status": 200, "message": "User get successfully"}

#READING THE USER BY ID
@user.get("/user/{user_id}")
def get_user(user_id: str,db: Session = Depends(get_db)):
   
    item = common_query(db,user_id).first()
    if item is not None:
        if item.is_delete==False:
        # return item
            return {"data": item, "status": 200, "message": "Users retrived successfully"}
        
        else:
            return("Message :" "User does not exist!")

#UPDATING THE USER
@user.put("/userput/{user_id}")
def update_user(user_id: str, user: UserSchema, db: Session = Depends(get_db)):

    user_to_update = common_query(db,user_id).first()
    user_to_update.user_name = user.user_name       
    db.commit()
    
    return {"status": 200, "message": "User Details updated successfully"}

#DELETING THE USER
@user.delete("/userdelete/{user_id}")
def delete_user(user_id: str,db: Session = Depends(get_db)):
   
    user_to_delete = common_query(db,user_id).first()
    if user_to_delete is not None:
        common_query(db,user_id).update({'is_delete':True})
        db.commit()
    
        return("User deleted successfully!")

#FETCH TOTAL NUMBER OF JOBS AND THE NAME OF THE JOB CREATED BY A PARTICULAR USER
@user.get("/usergetjob/{user_id}")
def total_jobs_created_by_a_particular_user(user_id: str, db: Session = Depends(get_db)):

    """get the job name and total jobs by specific user
    """
    job_count = common_filter(db, user_id).count()
    jobs = db.query(JobModel.job_name).filter(JobModel.created_by==user_id, JobModel.is_delete==False).all()
    
    return(f"total_jobs:{job_count}, job:{jobs}")






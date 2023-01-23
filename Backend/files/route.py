
from fastapi import APIRouter,Depends
from Backend.files.schema import FilesSchema
from Backend.files.model import FileModel
from sqlalchemy.orm import Session
from Backend.database.database import get_db

file = APIRouter()

def common_query(db,jobs_id):
    return db.query(FileModel).filter(FileModel.job_id == jobs_id,FileModel.is_delete==False)

def common_filter(db,file_id):
    return db.query(FileModel).filter(FileModel.id == file_id)

#CREATE A FILE AND SAVE IT TO DATABASE 
@file.post("/createfile/")
def create_file(file: FilesSchema,db: Session = Depends(get_db)):
    new_file = FileModel(file_name=file.file_name,job_id=file.job_id)
    db.add(new_file)
    db.commit()
    return {"status": 200, "message": "File added successfully"}

# FETCHING ALL THE FILES
@file.get("/file")
def read_all_files(db: Session = Depends(get_db)):

    user = db.query(FileModel).all()
    return {"data": user, "status": 200, "message": "All the files fetched  successfully"}

# FETCHING THE DATA OF ALL THE FILES THAT ARE CREATED FOR THE SAME JOB ID
@file.get("/file/{job_id}")
def read_file_by_job_id(jobs_id: str,db: Session = Depends(get_db)):
   
    item = common_query(db,jobs_id).all()
    if item is not None:
        return {"data": item, "status": 200, "message": "Files for a particular job id retrived successfully"}
    
    else:
        return("Message :" "File with given job id does not exist!")

# UPDATING THE FILES
@file.put("/fileput/{file_id}")
def update_file(file_id: str, file: FilesSchema, db: Session = Depends(get_db)):

    file_to_update = common_filter(db,file_id).first()
    if file_to_update is not None:
        if file_to_update.is_delete == False:
            data_dict = file.dict(exclude_unset=True)

            for key, value in data_dict.items():
                setattr(file_to_update, key, value)

            db.commit()
            return {"message": "File details updated successfully"}

        else:
            return "This File has been deleted earlier so the data cannot be updated."

    else:
        return "This File ID does not exists."

    
# DELETING THE FILE
@file.delete("/filedelete/{file_id}")
def delete_file(file_id: str,db: Session = Depends(get_db)):
   
    file_to_delete = common_filter(db,file_id).first()
    if file_to_delete is not None:
        common_filter(db,file_id).update({'is_delete':True})
        db.commit()
    
        return("File deleted successfully!")
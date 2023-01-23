from fastapi import APIRouter,Depends,File,UploadFile,Form,BackgroundTasks
from Backend.jobs.schema import JobSchema
from Backend.jobs.model import JobModel
from sqlalchemy.orm import Session
from Backend.database.database import get_db
# from Backend.jobs.models import train_model_bg
# from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pandas as pd
import asyncio
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix
import time


job = APIRouter()


def common_query(db,job_id):
    return db.query(JobModel).filter(JobModel.created_by == job_id, JobModel.is_delete==False)


def common_filter(db,job_id):
    return db.query(JobModel).filter(JobModel.id == job_id)


#CREATING THE JOB
@job.post("/jobpost")
def create_job(job: JobSchema,db: Session = Depends(get_db)):

    new_job = JobModel(job_name=job.job_name,input_features=job.input_features,output_features=job.output_features,algorithm=job.algorithm,created_by=job.created_by,updated_by=job.created_by)

    db.add(new_job)
    db.commit()
    return {"status": 200, "message": "Job created successfully"}


#READING THE JOB
@job.get("/job")
def get_all_jobs(db: Session = Depends(get_db)):

    job = db.query(JobModel).all()
    return {"data": job, "status": 200, "message": "Job fetched successfully!"}


#FETCHING THE JOB BY USER ID 
@job.get("/job/{user_id}")
def get_job_by_user_id(user_id: str,db: Session = Depends(get_db)):
   
    item = common_query(db,user_id).all()
    if item is not None:
  
      return {"data": item, "status": 200, "message": "Job retrived successfully"}
        
    else:
        return("Job with given id does not exist!")


#UPDATING THE JOB
@job.put("/jobput/{job_id}")
def update_job(job_id: str, job: JobSchema, db: Session = Depends(get_db)):

    job_to_update = common_filter(db,job_id).first()
    if job_to_update is not None:
        if job_to_update.is_delete == False:
            data_dict = job.dict(exclude_unset=True)

            for key, value in data_dict.items():
                setattr(job_to_update, key, value)

            db.commit()
            return {"message": "Job details updated successfully"}

        else:
            return "This job has been deleted earlier so the data cannot be updated."

    else:
        return "This ID does not exists."


#DELETING THE JOB
@job.delete("/jobdelete/{job_id}")
def delete_job(job_id: str,db: Session = Depends(get_db)):
   
    job_to_delete = common_filter(db,job_id).first()
    if job_to_delete is not None:
        common_filter(db,job_id).update({'is_delete':True})
        db.commit()
    
        return("Job deleted successfully!")


# Function to train the model
def train_logistic_regression_task():

    # read the data
    df=pd.read_csv('E:/WINTER_INTERNSHIP_REJOICE/FASTAPI_TASKS(2)/FastAPI_ML_Model/Backend/files/csv_files/IRIS.csv')
    x=df.iloc[:,:4]
    y=df.iloc[:,4]

    x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=0)
    # train the model
    model = LogisticRegression()
    model.fit(x_train, y_train)

    y_pred=model.predict(x_test)
    confusion_matrix(y_test,y_pred)
    accuracy=accuracy_score(y_test,y_pred)*100
    # ans = "{:.2f}".format(accuracy)
    
    print("Accuracy of the model is {:.2f}".format(accuracy))
    # save the model
    from joblib import dump, load
    dump(model, 'model.joblib')
    print("Training Completed")

    # return(ans)

#VALIDATING THE INPUTS AND THEN STARTING THE JOB IN THE BACKGROUND
@job.post("/startjob/{job_id}")
# async def start_job( job_id: str,bg_tasks : BackgroundTasks,file: UploadFile = File(...),user_input: str = Form(...),user_output:str=Form(...),db: Session = Depends(get_db)):
async def start_job( bg_tasks : BackgroundTasks,file: UploadFile = File(...),user_input: str = Form(...),user_output:str=Form(...)):


    # job_details=common_filter(db,job_id)
    # read the csv file and check with the user input
    df = pd.read_csv(file.file)
    column_names = list(df.columns)
    user_input_list = user_input.split(",")
    user_output_list = user_output.split(",")
    for col in (user_input_list and user_output_list):
        if col not in column_names:
            return {"error": "The value entered by the user is not present in the file , please update the file"}
    
        else:

            bg_tasks.add_task(train_logistic_regression_task)
            # common_filter(db,job_id).update({'accuracy':accuracy_value})
    
    return {"message": "Training task started"}




















# @router.post('/upload/')
# async def create_upload_file( bg_task : BackgroundTasks,file: UploadFile ,indepandant_columns: str = Form(...), depandant_column: str = Form(...), model_name : str = Form(...) , user_name : str = Form(...)):
#     db_query = db.query(UserData).filter(UserData.user_name == user_name).first()
#     if db_query is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="Please create user first")

#     if not file.filename.endswith('.csv'):
#         raise ValueError("Invalid file type, expected CSV.")

#     data = pd.read_csv(file.file)
#     input_columns = indepandant_columns.split(',')
#     csv_columns = data.columns.tolist()


#     if set(input_columns) == set(csv_columns) & depandant_column:
#         X = data.drop(depandant_column)
#         Y = data(depandant_column)
#         if model_name not in authorized_models:
#             raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail = "invalid model_name")
        
#         try:
#             global model
#             if data.model_name == Model_types.linear_regression:
#                 model = LinearRegression()

#             elif data.model_name == Model_types.logistic_regression:
#                 model = LogisticRegression(solver='lbfgs', max_iter=100)

#             bg_task.add_task(model.fit(X , Y))

#             model_id = str (uuid4())

#             model_directory = "models"
#             if not os.path.exists(model_directory):
#                 os.makedirs(model_directory)

#             model_path = os.path.join(model_directory, f"{model_id}.pkl")

#             new_job = JobData(
#                 job_id = model_id,
#                 job_name = model_name,
#                 user_name = user_name
#             )
#             db.add(new_job)
#             db.commit()

#             pickle.dump(model , open(model_path , 'wb'))
#             model_info = {"model_id" : model_id , "model_name" : model_name , "info" : "model is trained and created successfully"}

#         except Exception as e:
#             return {"status" : f"error while training: {e}"}
    

#     return JSONResponse(content = model_info)
#             #save the uploaded file in local
#             start_time = time.time()
#             # Training the model code
#             data = pd.read_csv(file.file)
#             X_train = data.iloc[:, :-1]
#             Y_train = data.iloc[:,-1:]

#             model=LogisticRegression()
#             model.fit(X_train , Y_train)
                    
#             await asyncio.sleep(10)
#             end_time = time.time()
#             elapsed_time = end_time - start_time
#             estimated_time = round(elapsed_time,2)
#             print(f"Model training completed in {estimated_time} seconds")
#             return {"estimated_time": estimated_time}


#     # start the background task
#     # bg_tasks = BackgroundTasks()
#     # bg_tasks.add_task(train_model_bg)
#     # return {"message": "Model training started in the background"}  #Status Code


    
#     # if model_name not in authorized_models:
#     #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail = "invalid model_name")
        
#     #     try:
#     #         global model
#     #         if data.model_name == Model_types.linear_regression:
#     #             model = LinearRegression()

#     #         elif data.model_name == Model_types.logistic_regression:
#     #             model = LogisticRegression(solver='lbfgs', max_iter=100)

#     #         bg_task.add_task(model.fit(X , Y))

#     #         model_id = str (uuid4())

#     #         model_directory = "models"
#     #         if not os.path.exists(model_directory):
#     #             os.makedirs(model_directory)

#             # model_path = os.path.join(model_directory, f"{model_id}.pkl")

#             # new_job = JobData(
#             #     job_id = model_id,
#             #     job_name = model_name,
#             #     user_name = user_name
#             #)
#         #     db.add(new_job)
#         #     db.commit()

#         #     pickle.dump(model , open(model_path , 'wb'))
#         #     model_info = {"model_id" : model_id , "model_name" : model_name , "info" : "model is trained and created successfully"}

#         # except Exception as e:
#         #     return {"status" : f"error while training: {e}"}
    

#     # return JSONResponse(content = model_info)
# # async def train_model_bg(file,X_train, Y_train):
    
    
    
#     # print("Model training started...")
#     # y_pred = clf.predict(X_test)
#     # acc = accuracy_score(y_test, y_pred)
#     # print(acc)



# # @job.get("/job/result")
# # async def job_result():
# #     # retrieve the result of the job
# #     result = get_job_result()
# #     return result

# # @job.get("/job/download")
# # async def job_download():
# #     # return the trained model file for download
# #     return FileResponse(os.path.join('app/models', 'trained_model.sav'))

# # CALCULATING ESTIMATED TIME

































































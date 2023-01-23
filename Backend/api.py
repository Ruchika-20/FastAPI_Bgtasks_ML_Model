from fastapi import FastAPI
from Backend.users.route import user
from Backend.jobs.route import job
from Backend.files.route import file

app = FastAPI()

app.include_router(user, tags=["users"])
app.include_router(job, tags=["jobs"])
app.include_router(file, tags=["files"])

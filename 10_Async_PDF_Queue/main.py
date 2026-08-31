from fastapi import FastAPI
from pydantic import BaseModel
import uuid

from job_queue import add_job, get_jobs


app = FastAPI(
    title="Async PDF Processing API",
    description="A simple PDF job queue API",
    version="1.0.0"
)


class PDFJob(BaseModel):
    filename: str


@app.get("/")
def home():
    return {
        "message": "Async PDF Processing API is running"
    }


@app.post("/jobs")
def create_job(job: PDFJob):

    new_job = {
        "id": str(uuid.uuid4()),
        "file": job.filename,
        "status": "pending"
    }

    add_job(new_job)

    return {
        "message": "PDF job added successfully",
        "job": new_job
    }


@app.get("/jobs")
def list_jobs():

    return {
        "jobs": get_jobs()
    }
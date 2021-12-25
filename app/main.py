# https://fastapi.tiangolo.com/tutorial/first-steps/
# How to run the code: uvicorn app.main:app --reload

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import (
    employee_type,
    employee,
    auth,
    initiative_type,
    status_code,
    initiative,
    task_log,
    review,
    rating
)


app = FastAPI(
    title="Task and Reward API",
    description="A simple API for keeping track of tasks and rewards",
    version="0.1.0",
    contact={
        "name": "Kamal",
        "url": "https://github.com/KamalDGRT"
    }
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee_type.router)
app.include_router(employee.router)
app.include_router(auth.router)
app.include_router(initiative_type.router)
app.include_router(status_code.router)
app.include_router(initiative.router)
app.include_router(task_log.router)
app.include_router(review.router)
app.include_router(rating.router)


@app.get("/")
async def root():
    return {
        "message": "API is running successfully!"
    }

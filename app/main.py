# https://fastapi.tiangolo.com/tutorial/first-steps/
# How to run the code: uvicorn app.main:app --reload

from fastapi import FastAPI


from app.database import SQLALCHEMY_DATABASE_URL

print(SQLALCHEMY_DATABASE_URL)

app = FastAPI(
    title="Task and Reward API",
    description="A simple API for keeping track of tasks and rewards",
    version="0.1.0",
    contact={
        "name": "Kamal",
        "url": "https://github.com/KamalDGRT"
    }
)


@app.get("/")
async def root():
    return {
        "message": "API is running successfully!"
    }

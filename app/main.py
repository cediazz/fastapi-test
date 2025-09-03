from fastapi import FastAPI
from .database import create_tables

app = FastAPI(
    title="Task API",
    description="A REST API for managing tasks with authentication",
    version="1.0.0"
)

#create tables
@app.on_event("startup")
async def on_startup():
    await create_tables()


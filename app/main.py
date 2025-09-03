from fastapi import FastAPI
from .database import create_tables
from .routes.user_routes import users_routers

app = FastAPI(
    title="Task API",
    description="A REST API for managing tasks with authentication",
    version="1.0.0"
)
app.include_router(users_routers)

#create tables
@app.on_event("startup")
async def on_startup():
    await create_tables()


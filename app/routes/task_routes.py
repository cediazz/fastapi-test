from fastapi import APIRouter,Depends, Query
from ..schemas import task_schemas
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_async_session
from .. import models
from ..services.task_services import TaskService
from .. import auth
from typing import List
from ..dependencies import get_task_service

task_routers = APIRouter(
    prefix="/task",
    tags=["tasks"],
    dependencies=[
        Depends(auth.oauth2_scheme)
    ]
)

@task_routers.post("/", response_model=task_schemas.TaskResponse)
async def create_task(
    task: task_schemas.TaskCreate,
    current_user: models.User = Depends(auth.get_current_active_user),
    session: AsyncSession = Depends(get_async_session),
    task_service: TaskService = Depends(get_task_service)
):
    return await task_service.create_user_task(session, task, current_user.id)

@task_routers.get("/", response_model=List[task_schemas.TaskResponse])
async def list_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: models.User = Depends(auth.get_current_active_user),
    session: AsyncSession = Depends(get_async_session),
    task_service: TaskService = Depends(get_task_service)
):
    return await task_service.get_user_tasks(session, current_user.id, skip=skip, limit=limit)

@task_routers.get("/{id}", response_model=task_schemas.TaskResponse)
async def get_task(
    id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    session: AsyncSession = Depends(get_async_session),
    task_service: TaskService = Depends(get_task_service)
):
   return await task_service.get_task_by_id(session, id, current_user.id)

@task_routers.put("/{task_id}", response_model=task_schemas.TaskResponse)
async def update_task(
    task_update: task_schemas.TaskUpdate,
    task_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    session: AsyncSession = Depends(get_async_session),
    task_service: TaskService = Depends(get_task_service)
):
    return await task_service.update_task(session, task_id, task_update, current_user.id)
    

@task_routers.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    session: AsyncSession = Depends(get_async_session),
    task_service: TaskService = Depends(get_task_service)
):
    return await task_service.delete_task(session, task_id, current_user.id)
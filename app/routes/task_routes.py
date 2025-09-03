from fastapi import APIRouter,Depends
from ..schemas import task_schemas
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_async_session
from .. import models
from ..services.task_services import TaskService
from .. import auth


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
    session: AsyncSession = Depends(get_async_session)
):
    return await TaskService().create_user_task(session, task, current_user.id)

"""@app.get("/tasks", response_model=List[schemas.TaskResponse])
async def read_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    completed: Optional[bool] = None,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    tasks = await crud.get_user_tasks(db, current_user.id, skip=skip, limit=limit)
    
    if completed is not None:
        tasks = [task for task in tasks if task.completed == completed]
    
    return tasks

@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def read_task(task: models.Task = Depends(verify_task_ownership)):
    return task

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def update_task(
    task_update: schemas.TaskUpdate,
    task_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    updated_task = await crud.update_task(db, task_id, task_update, current_user.id)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or access denied"
        )
    return updated_task

@app.delete("/tasks/{task_id}")
async def delete_task(
    task_id: int,
    current_user: models.User = Depends(auth.get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    success = await crud.delete_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or access denied"
        )
    return {"message": "Task deleted successfully"}"""
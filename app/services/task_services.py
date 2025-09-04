from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update,delete
from .. import models
from ..schemas import task_schemas
from fastapi import HTTPException

class TaskService:
    
    async def get_user_tasks(
        self,
        session: AsyncSession, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ):
        result = await session.execute(
            select(models.Task)
            .where(models.Task.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .order_by(models.Task.created_at.desc())
            )
        return result.scalars().all()
    
    async def get_task_by_id(
        self, 
        session: AsyncSession, 
        task_id: int, 
        user_id: int
    ):
        result = await session.execute(
            select(models.Task)
            .where(models.Task.id == task_id)
            .where(models.Task.user_id == user_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=400, detail="Invalid task id")
        return task
    
    async def create_user_task(
        self, 
        session: AsyncSession, 
        task: task_schemas.TaskCreate,
        user_id : int
    ):
        db_task = models.Task(**task.model_dump(), user_id=user_id)
        session.add(db_task)
        await session.commit()
        await session.refresh(db_task)
        return db_task
    
    async def update_task(
        self, 
        session: AsyncSession, 
        task_id: int, 
        task_update: task_schemas.TaskUpdate, 
        user_id: int
    ):
        stmt = (
        update(models.Task)
        .where(models.Task.id == task_id, models.Task.user_id == user_id)
        .values(**task_update.model_dump(exclude_unset=True))
        .returning(models.Task)
        )
        result = await session.execute(stmt)
        task = result.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=400, detail="Invalid task id")
        await session.commit()
        await session.refresh(task)
        return task
    
    async def delete_task(
        self, 
        session: AsyncSession, 
        task_id: int, 
        user_id: int
    ):
        result = await session.execute(
        delete(models.Task)
        .where(models.Task.id == task_id, models.Task.user_id == user_id)
        .returning(models.Task.id)
        )
        task = result.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=400, detail="Invalid task id")
        await session.commit()
        return {"message": "Task deleted successfully"}
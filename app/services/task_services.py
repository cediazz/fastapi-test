from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete
from .. import models
from ..schemas import task_schemas
from fastapi import HTTPException,Depends
from ..services.user_services import UserService

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
        return result.scalar_one_or_none()
    
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
        existing_task = await self.get_task_by_id(session, task_id, user_id)
        if not existing_task:
            raise HTTPException(status_code=400, detail="Invalid task id")
        update_data = task_update.model_dump(exclude_unset=True)
        existing_task.title = update_data['title']
        existing_task.description = update_data['description']
        existing_task.completed = update_data['completed']
        await session.commit()
        await session.refresh(existing_task)
        return existing_task
    
    async def delete_task(
        self, 
        session: AsyncSession, 
        task_id: int, 
        user_id: int
    ):
        result = await session.execute(
            delete(models.Task)
            .where(models.Task.id == task_id)
            .where(models.Task.user_id == user_id)
    )
        await session.commit()
        return result.rowcount > 0
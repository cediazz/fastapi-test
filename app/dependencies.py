from .services.task_services import TaskService

def get_task_service():
    return TaskService()
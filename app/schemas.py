from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from app.models import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Título da tarefa",
        examples=["Implementar testes unitários"],
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Descrição detalhada da tarefa",
        examples=["Criar testes com pytest para os endpoints de tarefas"],
    )
    status: TaskStatus = Field(
        default=TaskStatus.TODO,
        description="Status atual da tarefa",
        examples=[TaskStatus.TODO],
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM,
        description="Nível de prioridade",
        examples=[TaskPriority.HIGH],
    )


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None


class TaskResponse(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    total: int = Field(..., description="Número total de itens correspondentes")
    page: int = Field(..., description="Página atual (base 1)")
    size: int = Field(..., description="Tamanho da página")
    items: list[TaskResponse] = Field(..., description="Lista de tarefas")


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str

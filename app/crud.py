from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.models import Task, TaskStatus, TaskPriority
from app.schemas import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int) -> Optional[Task]:
    """Busca uma tarefa por ID."""
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    search: Optional[str] = None,
) -> tuple[list[Task], int]:
    """
    Lista tarefas com suporte a filtros por status, prioridade,
    busca textual no título e paginação.
    Retorna uma tupla (items, total_count).
    """
    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    total = query.count()
    items = query.order_by(Task.id.desc()).offset(skip).limit(limit).all()
    return items, total


def create_task(db: Session, task_in: TaskCreate) -> Task:
    """Cria uma nova tarefa no banco de dados."""
    db_task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status,
        priority=task_in.priority,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, db_task: Task, task_in: TaskUpdate) -> Task:
    """Atualiza campos fornecidos de uma tarefa existente."""
    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, db_task: Task) -> None:
    """Remove uma tarefa do banco de dados."""
    db.delete(db_task)
    db.commit()

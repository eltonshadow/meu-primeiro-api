from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import TaskStatus, TaskPriority
from app.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
)
from app import crud

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar uma nova tarefa",
)
def create_task_endpoint(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
) -> TaskResponse:
    """Cria uma nova tarefa com título, descrição, status e prioridade."""
    return crud.create_task(db=db, task_in=task_in)


@router.get(
    "",
    response_model=TaskListResponse,
    summary="Listar tarefas",
)
def list_tasks_endpoint(
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Quantidade por página"),
    status: Optional[TaskStatus] = Query(None, description="Filtrar por status"),
    priority: Optional[TaskPriority] = Query(None, description="Filtrar por prioridade"),
    search: Optional[str] = Query(None, description="Buscar termo no título"),
    db: Session = Depends(get_db),
) -> TaskListResponse:
    """Retorna lista paginada de tarefas com filtros opcionais."""
    skip = (page - 1) * size
    items, total = crud.get_tasks(
        db=db,
        skip=skip,
        limit=size,
        status=status,
        priority=priority,
        search=search,
    )
    return TaskListResponse(
        total=total,
        page=page,
        size=size,
        items=items,
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Buscar tarefa por ID",
)
def get_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
) -> TaskResponse:
    """Retorna os dados de uma tarefa específica."""
    task = crud.get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {task_id} não encontrada.",
        )
    return task


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Atualizar tarefa completamente",
)
def update_task_endpoint(
    task_id: int,
    task_in: TaskCreate,
    db: Session = Depends(get_db),
) -> TaskResponse:
    """Substitui os dados da tarefa especificada."""
    task = crud.get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {task_id} não encontrada.",
        )
    update_data = TaskUpdate(**task_in.model_dump())
    return crud.update_task(db=db, db_task=task, task_in=update_data)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Atualizar parcialmente uma tarefa",
)
def patch_task_endpoint(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
) -> TaskResponse:
    """Atualiza apenas os campos enviados no corpo da requisição."""
    task = crud.get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {task_id} não encontrada.",
        )
    return crud.update_task(db=db, db_task=task, task_in=task_in)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar uma tarefa",
)
def delete_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
) -> None:
    """Remove a tarefa especificada por ID."""
    task = crud.get_task(db=db, task_id=task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {task_id} não encontrada.",
        )
    crud.delete_task(db=db, db_task=task)
    return None

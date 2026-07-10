from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app import models
from app.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])


class TaskCreate(BaseModel):
    title: str


class TaskResponse(BaseModel):
    id: int
    title: str
    done: bool
    owner_id: int
    completed_by_id: int | None

    model_config = {"from_attributes": True}


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    task = models.Task(title=payload.title, owner_id=current_user.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/mine", response_model=list[TaskResponse])
def get_my_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Task)
        .filter(
            models.Task.owner_id == current_user.id,
            models.Task.done.is_(False),
        )
        .all()
    )


@router.get("/theirs", response_model=list[TaskResponse])
def get_their_tasks(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return (
        db.query(models.Task)
        .filter(
            models.Task.owner_id != current_user.id,
            models.Task.done.is_(False),
        )
        .all()
    )


@router.patch("/{task_id}/done", response_model=TaskResponse)
def mark_done(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.done = True  # type: ignore
    task.completed_by_id = current_user.id  # type: ignore
    db.commit()
    db.refresh(task)
    return task


@router.patch("/{task_id}/claim", response_model=TaskResponse)
def claim_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id == current_user.id:  # type: ignore
        raise HTTPException(
            status_code=400, detail="That task is already yours"
        )
    task.owner_id = current_user.id
    db.commit()
    db.refresh(task)
    return task

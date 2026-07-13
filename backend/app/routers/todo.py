from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated
from app.database import get_db
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoToggle, TodoOut
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/todos", tags=["Todos"])


def make_response(code: int = 200, message: str = "ok", data=None):
    return {"code": code, "message": message, "data": data}


@router.get("", response_model=dict)
def list_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    urgency: Annotated[str | None, Query()] = None,
    completed: Annotated[bool | None, Query()] = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(Todo).filter(Todo.user_id == current_user.id)
    if urgency:
        query = query.filter(Todo.urgency == urgency)
    if completed is not None:
        query = query.filter(Todo.completed == completed)
    total = query.count()
    items = (
        query.order_by(Todo.completed.asc(), Todo.deadline.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return make_response(
        data={"total": total, "items": [TodoOut.model_validate(i) for i in items]}
    )


@router.get("/{todo_id}", response_model=dict)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Todo not found")
    return make_response(data=TodoOut.model_validate(item))


@router.post("", response_model=dict)
def create_todo(
    todo_in: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = Todo(
        user_id=current_user.id,
        title=todo_in.title,
        urgency=todo_in.urgency,
        deadline=todo_in.deadline,
        completed=todo_in.completed,
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return make_response(data=TodoOut.model_validate(todo))


@router.put("/{todo_id}", response_model=dict)
def update_todo(
    todo_id: int,
    todo_in: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == current_user.id)
        .first()
    )
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.title = todo_in.title
    todo.urgency = todo_in.urgency
    todo.deadline = todo_in.deadline
    todo.completed = todo_in.completed
    db.commit()
    db.refresh(todo)
    return make_response(data=TodoOut.model_validate(todo))


@router.patch("/{todo_id}/complete", response_model=dict)
def toggle_complete(
    todo_id: int,
    payload: TodoToggle,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == current_user.id)
        .first()
    )
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.completed = payload.completed
    db.commit()
    db.refresh(todo)
    return make_response(data=TodoOut.model_validate(todo))


@router.delete("/{todo_id}", response_model=dict)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == current_user.id)
        .first()
    )
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return make_response(message="Todo deleted")

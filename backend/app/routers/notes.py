from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated
from app.database import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate, NoteOut
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/notes", tags=["Notes"])


def make_response(code: int = 200, message: str = "ok", data=None):
    return {"code": code, "message": message, "data": data}


@router.get("", response_model=dict)
def list_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    q: Annotated[str | None, Query()] = None,
    tag: Annotated[str | None, Query()] = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(Note).filter(Note.user_id == current_user.id)
    if q:
        query = query.filter(Note.title.contains(q) | Note.content.contains(q))
    if tag:
        query = query.filter(Note.tags.contains(tag))
    total = query.count()
    notes = query.order_by(Note.created_at.desc()).offset(skip).limit(limit).all()
    return make_response(
        data={"total": total, "items": [NoteOut.model_validate(n) for n in notes]}
    )


@router.get("/{note_id}", response_model=dict)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == current_user.id)
        .first()
    )
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return make_response(data=NoteOut.model_validate(note))


@router.post("", response_model=dict)
def create_note(
    note_in: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = Note(
        user_id=current_user.id,
        title=note_in.title,
        content=note_in.content,
        tags=note_in.tags,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return make_response(data=NoteOut.model_validate(note))


@router.put("/{note_id}", response_model=dict)
def update_note(
    note_id: int,
    note_in: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == current_user.id)
        .first()
    )
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = note_in.title
    note.content = note_in.content
    note.tags = note_in.tags
    db.commit()
    db.refresh(note)
    return make_response(data=NoteOut.model_validate(note))


@router.delete("/{note_id}", response_model=dict)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.user_id == current_user.id)
        .first()
    )
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return make_response(message="Note deleted")

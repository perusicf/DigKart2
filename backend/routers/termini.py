from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas, crud

router = APIRouter()

@router.get("/", response_model=List[schemas.TerminOut])
def list_termini(db: Session = Depends(get_db)):
    return crud.get_all_termini(db)

@router.get("/{termin_id}", response_model=schemas.TerminOut)
def get_termin(termin_id: int, db: Session = Depends(get_db)):
    termin = crud.get_termin(db, termin_id)
    if not termin:
        raise HTTPException(status_code=404, detail="Termin not found")
    return termin

@router.post("/", response_model=schemas.TerminOut, status_code=201)
def create_termin(termin: schemas.TerminCreate, db: Session = Depends(get_db)):
    return crud.create_termin(db, termin)

@router.delete("/{termin_id}", response_model=schemas.TerminOut)
def delete_termin(termin_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_termin(db, termin_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Termin not found")
    return deleted

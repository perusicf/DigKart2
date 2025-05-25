from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import schemas, crud

router = APIRouter()

@router.get("/", response_model=List[schemas.PacijentOut])
def list_pacijenti(db: Session = Depends(get_db)):
    return crud.get_all_pacijenti(db)

@router.get("/{pacijent_id}", response_model=schemas.PacijentOut)
def get_pacijent(pacijent_id: int, db: Session = Depends(get_db)):
    pacijent = crud.get_pacijent(db, pacijent_id)
    if not pacijent:
        raise HTTPException(status_code=404, detail="Pacijent not found")
    return pacijent

@router.post("/", response_model=schemas.PacijentOut, status_code=201)
def create_pacijent(pacijent: schemas.PacijentCreate, db: Session = Depends(get_db)):
    return crud.create_pacijent(db, pacijent)

@router.delete("/{pacijent_id}", response_model=schemas.PacijentOut)
def delete_pacijent(pacijent_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_pacijent(db, pacijent_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Pacijent not found")
    return deleted

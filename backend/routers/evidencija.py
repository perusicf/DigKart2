from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas, crud

router = APIRouter()

@router.post("/", response_model=schemas.EvidencijaOut, status_code=201)
def log_access(evidencija: schemas.EvidencijaCreate, db: Session = Depends(get_db)):
    return crud.create_evidencija(db, evidencija)

@router.get("/", response_model=List[schemas.EvidencijaOut])
def list_evidencije(db: Session = Depends(get_db)):
    return crud.get_all_evidencije(db)

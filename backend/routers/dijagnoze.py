from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas, crud

router = APIRouter()

@router.get("/", response_model=List[schemas.DijagnozaOut])
def list_dijagnoze(db: Session = Depends(get_db)):
    return crud.get_all_dijagnoze(db)

@router.get("/{dijagnoza_id}", response_model=schemas.DijagnozaOut)
def get_dijagnoza(dijagnoza_id: int, db: Session = Depends(get_db)):
    dijagnoza = crud.get_dijagnoza(db, dijagnoza_id)
    if not dijagnoza:
        raise HTTPException(status_code=404, detail="Dijagnoza not found")
    return dijagnoza

@router.post("/", response_model=schemas.DijagnozaOut, status_code=201)
def create_dijagnoza(dijagnoza: schemas.DijagnozaCreate, db: Session = Depends(get_db)):
    return crud.create_dijagnoza(db, dijagnoza)

@router.delete("/{dijagnoza_id}", response_model=schemas.DijagnozaOut)
def delete_dijagnoza(dijagnoza_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_dijagnoza(db, dijagnoza_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Dijagnoza not found")
    return deleted

@router.put("/{dijagnoza_id}", response_model=schemas.DijagnozaOut)
def update_dijagnoza(
    dijagnoza_id: int,
    dijagnoza: schemas.DijagnozaUpdate,
    db: Session = Depends(get_db)
):
    db_dijagnoza = crud.update_dijagnoza(db, dijagnoza_id, dijagnoza)
    if db_dijagnoza is None:
        raise HTTPException(status_code=404, detail="Dijagnoza not found")
    return db_dijagnoza

@router.get("/karton/{karton_id}", response_model=List[schemas.DijagnozaOut])
def get_dijagnoze_by_karton_id(
    karton_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_dijagnoze_by_karton_id(db, karton_id)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas, crud
import models

router = APIRouter()

@router.get("/", response_model=List[schemas.KartonOut])
def list_kartoni(db: Session = Depends(get_db)):
    return crud.get_all_kartoni(db)

@router.get("/{karton_id}", response_model=schemas.KartonOut)
def get_karton(karton_id: int, db: Session = Depends(get_db)):
    karton = crud.get_karton(db, karton_id)
    if not karton:
        raise HTTPException(status_code=404, detail="Karton not found")
    return karton

@router.post("/", response_model=schemas.KartonOut, status_code=201)
def create_karton(karton: schemas.KartonCreate, db: Session = Depends(get_db)):
    return crud.create_karton(db, karton)

@router.delete("/{karton_id}", response_model=schemas.KartonOut)
def delete_karton(karton_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_karton(db, karton_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Karton not found")
    return deleted

@router.get("/pacijent/{pacijent_id}", response_model=List[schemas.KartonOut])
def get_kartoni_for_pacijent(pacijent_id: int, db: Session = Depends(get_db)):
    kartoni = db.query(models.Karton).filter(models.Karton.pacijent_id == pacijent_id).all()
    if not kartoni:
        return []
    return kartoni


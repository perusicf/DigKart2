from fastapi import APIRouter, Depends, HTTPException
from fastapi import Query, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import schemas, crud

router = APIRouter()

@router.get("/", response_model=List[schemas.TerapijaOut])
def list_terapije(db: Session = Depends(get_db)):
    return crud.get_all_terapije(db)

@router.get("/{terapija_id}", response_model=schemas.TerapijaOut)
def get_terapija(terapija_id: int, db: Session = Depends(get_db)):
    terapija = crud.get_terapija(db, terapija_id)
    if not terapija:
        raise HTTPException(status_code=404, detail="Terapija not found")
    return terapija



@router.post("/", response_model=schemas.TerapijaOut, status_code=201)
def create_terapija(
    terapija: schemas.TerapijaCreate,
    db: Session = Depends(get_db),
    role: str = Query(..., description="User role (e.g. lijecnik, administrator)")
):
    if role not in ["lijecnik", "administrator"]:
        raise HTTPException(status_code=403, detail="Access denied")

    return crud.create_terapija(db, terapija)


@router.delete("/{terapija_id}", response_model=schemas.TerapijaOut)
def delete_terapija(terapija_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_terapija(db, terapija_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Terapija not found")
    return deleted

@router.put("/{terapija_id}", response_model=schemas.TerapijaOut)
def update_terapija(
    terapija_id: int,
    terapija: schemas.TerapijaUpdate,
    db: Session = Depends(get_db)
):
    db_terapija = crud.update_terapija(db, terapija_id, terapija)
    if db_terapija is None:
        raise HTTPException(status_code=404, detail="Terapija not found")
    return db_terapija

@router.get("/dijagnoza/{dijagnoza_id}", response_model=List[schemas.TerapijaOut])
def get_terapije_by_dijagnoza(dijagnoza_id: int, db: Session = Depends(get_db)):
    return crud.get_terapije_by_dijagnoza(db, dijagnoza_id)


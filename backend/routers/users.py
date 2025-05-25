from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import get_db
from models import Korisnik
from auth import verify_password
from typing import List
import schemas, crud

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Korisnik).filter(Korisnik.korisnicko_ime == data.username).first()
    if not user or not verify_password(data.password, user.lozinka):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {
        "message": "Login successful",
        "user_id": user.korisnik_id,
        "role": user.uloga,
        "ime": user.ime,
        "prezime": user.prezime
    }


@router.get("/", response_model=List[schemas.KorisnikOut])
def list_users(db: Session = Depends(get_db)):
    return crud.get_all_korisnici(db)

@router.get("/{korisnik_id}", response_model=schemas.KorisnikOut)
def get_user(korisnik_id: int, db: Session = Depends(get_db)):
    user = crud.get_korisnik_by_id(db, korisnik_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=schemas.KorisnikOut, status_code=201)
def create_user(user: schemas.KorisnikCreate, db: Session = Depends(get_db)):
    return crud.create_korisnik(db, user)

@router.put("/{korisnik_id}", response_model=schemas.KorisnikOut)
def update_user(korisnik_id: int, user: schemas.KorisnikUpdate, db: Session = Depends(get_db)):
    updated = crud.update_korisnik(db, korisnik_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{korisnik_id}", response_model=schemas.KorisnikOut)
def delete_user(korisnik_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_korisnik(db, korisnik_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted

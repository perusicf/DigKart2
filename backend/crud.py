from sqlalchemy.orm import Session
from models import Pacijent
from schemas import PacijentCreate
from sqlalchemy.orm import Session
import models
import schemas
import models
import schemas
from models import Korisnik  



# Get all patients
def get_all_pacijenti(db: Session):
    return db.query(Pacijent).all()

# Get single patient by ID
def get_pacijent(db: Session, pacijent_id: int):
    return db.query(Pacijent).filter(Pacijent.pacijent_id == pacijent_id).first()

# Create new patient
def create_pacijent(db: Session, pacijent: PacijentCreate):
    db_pacijent = Pacijent(**pacijent.dict())
    db.add(db_pacijent)
    db.commit()
    db.refresh(db_pacijent)
    return db_pacijent

# Delete patient
def delete_pacijent(db: Session, pacijent_id: int):
    pacijent = get_pacijent(db, pacijent_id)
    if pacijent:
        db.delete(pacijent)
        db.commit()
    return pacijent

from models import Karton
from schemas import KartonCreate

def get_all_kartoni(db: Session):
    return db.query(Karton).all()

def get_karton(db: Session, karton_id: int):
    return db.query(Karton).filter(Karton.karton_id == karton_id).first()

def create_karton(db: Session, karton: KartonCreate):
    db_karton = Karton(**karton.dict())
    db.add(db_karton)
    db.commit()
    db.refresh(db_karton)
    return db_karton

def delete_karton(db: Session, karton_id: int):
    karton = get_karton(db, karton_id)
    if karton:
        db.delete(karton)
        db.commit()
    return karton


from models import Dijagnoza
from schemas import DijagnozaCreate
from schemas import DijagnozaUpdate

def get_all_dijagnoze(db: Session):
    return db.query(Dijagnoza).all()

def get_dijagnoza(db: Session, dijagnoza_id: int):
    return db.query(Dijagnoza).filter(Dijagnoza.dijagnoza_id == dijagnoza_id).first()

def create_dijagnoza(db: Session, dijagnoza: DijagnozaCreate):
    db_dijagnoza = Dijagnoza(**dijagnoza.dict())
    db.add(db_dijagnoza)
    db.commit()
    db.refresh(db_dijagnoza)
    return db_dijagnoza

def delete_dijagnoza(db: Session, dijagnoza_id: int):
    dijagnoza = get_dijagnoza(db, dijagnoza_id)
    if dijagnoza:
        db.delete(dijagnoza)
        db.commit()
    return dijagnoza

def update_dijagnoza(db: Session, dijagnoza_id: int, updated_data: schemas.DijagnozaUpdate):
    dijagnoza = db.query(Dijagnoza).filter(Dijagnoza.dijagnoza_id == dijagnoza_id).first()
    if dijagnoza:
        dijagnoza.opis_dijagnoze = updated_data.opis_dijagnoze
        dijagnoza.datum_dijagnoze = updated_data.datum_dijagnoze
        db.commit()
        db.refresh(dijagnoza)
    return dijagnoza

def get_dijagnoze_by_karton_id(db: Session, karton_id: int):
    return db.query(Dijagnoza).filter(Dijagnoza.karton_id == karton_id).all()


from models import Terapija
from schemas import TerapijaCreate

def get_all_terapije(db: Session):
    return db.query(Terapija).all()

def get_terapija(db: Session, terapija_id: int):
    return db.query(Terapija).filter(Terapija.terapija_id == terapija_id).first()

def create_terapija(db: Session, terapija: TerapijaCreate):
    db_terapija = Terapija(**terapija.dict())
    db.add(db_terapija)
    db.commit()
    db.refresh(db_terapija)
    return db_terapija

def delete_terapija(db: Session, terapija_id: int):
    terapija = get_terapija(db, terapija_id)
    if terapija:
        db.delete(terapija)
        db.commit()
    return terapija

def update_terapija(db: Session, terapija_id: int, updated_data: schemas.TerapijaUpdate):
    terapija = db.query(Terapija).filter(Terapija.terapija_id == terapija_id).first()
    if terapija:
        terapija.opis_terapije = updated_data.opis_terapije
        db.commit()
        db.refresh(terapija)
    return terapija

def get_terapije_by_dijagnoza(db: Session, dijagnoza_id: int):
    return db.query(Terapija).filter(Terapija.dijagnoza_id == dijagnoza_id).all()


from models import Termin
from schemas import TerminCreate

def get_all_termini(db: Session):
    return db.query(Termin).all()

def get_termin(db: Session, termin_id: int):
    return db.query(Termin).filter(Termin.termin_id == termin_id).first()

def create_termin(db: Session, termin: TerminCreate):
    db_termin = Termin(**termin.dict())
    db.add(db_termin)
    db.commit()
    db.refresh(db_termin)
    return db_termin

def delete_termin(db: Session, termin_id: int):
    termin = get_termin(db, termin_id)
    if termin:
        db.delete(termin)
        db.commit()
    return termin

from models import EvidencijaPristupa
from schemas import EvidencijaCreate

def create_evidencija(db: Session, evidencija: EvidencijaCreate):
    db_evidencija = EvidencijaPristupa(**evidencija.dict())
    db.add(db_evidencija)
    db.commit()
    db.refresh(db_evidencija)
    return db_evidencija

def get_all_evidencije(db: Session):
    return db.query(EvidencijaPristupa).all()

from auth import hash_password

def get_all_korisnici(db: Session):
    return db.query(Korisnik).all()

def get_korisnik_by_id(db: Session, korisnik_id: int):
    return db.query(Korisnik).filter(Korisnik.korisnik_id == korisnik_id).first()

def create_korisnik(db: Session, user_data: schemas.KorisnikCreate):
    hashed_pw = hash_password(user_data.lozinka)
    db_user = Korisnik(
        korisnicko_ime=user_data.korisnicko_ime,
        lozinka=hashed_pw,
        ime=user_data.ime,
        prezime=user_data.prezime,
        uloga=user_data.uloga
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_korisnik(db: Session, korisnik_id: int, user_data: schemas.KorisnikUpdate):
    user = get_korisnik_by_id(db, korisnik_id)
    if not user:
        return None
    if user_data.ime:
        user.ime = user_data.ime
    if user_data.prezime:
        user.prezime = user_data.prezime
    if user_data.lozinka:
        user.lozinka = hash_password(user_data.lozinka)
    if user_data.uloga:
        user.uloga = user_data.uloga
    db.commit()
    db.refresh(user)
    return user

def delete_korisnik(db: Session, korisnik_id: int):
    user = get_korisnik_by_id(db, korisnik_id)
    if not user:
        return None
    db.delete(user)
    db.commit()
    return user

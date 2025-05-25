from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


# ───── PACIJENT ─────
class PacijentBase(BaseModel):
    oib: str = Field(..., min_length=11, max_length=11)
    ime: str
    prezime: str
    kontakt: Optional[str] = None


class PacijentCreate(PacijentBase):
    pass


class PacijentOut(PacijentBase):
    pacijent_id: int

    class Config:
        orm_mode = True


# ───── KARTON ─────
class KartonBase(BaseModel):
    datum_otvaranja: Optional[date] = None
    status_aktivnosti: str


class KartonCreate(KartonBase):
    pacijent_id: int


class KartonOut(KartonBase):
    karton_id: int
    pacijent_id: int

    class Config:
        orm_mode = True


class KorisnikBase(BaseModel):
    korisnicko_ime: str
    ime: str
    prezime: str
    uloga: str

class KorisnikCreate(KorisnikBase):
    lozinka: str  # plain password to be hashed

class KorisnikUpdate(BaseModel):
    ime: str | None = None
    prezime: str | None = None
    lozinka: str | None = None
    uloga: str | None = None

class KorisnikOut(KorisnikBase):
    korisnik_id: int

    class Config:
        from_attributes = True


# ───── DIJAGNOZA ─────
class DijagnozaBase(BaseModel):
    opis_dijagnoze: str
    datum_dijagnoze: Optional[date] = None


class DijagnozaCreate(DijagnozaBase):
    karton_id: int
    lijecnik_id: int


class DijagnozaOut(DijagnozaBase):
    dijagnoza_id: int
    karton_id: int
    lijecnik_id: int

    class Config:
        orm_mode = True


# ───── TERAPIJA ─────
class TerapijaBase(BaseModel):
    opis_terapije: str


class TerapijaCreate(TerapijaBase):
    dijagnoza_id: int
    lijecnik_id: int


class TerapijaOut(TerapijaBase):
    terapija_id: int
    dijagnoza_id: int
    lijecnik_id: int

class TerapijaUpdate(BaseModel):
    opis_terapije: str


    class Config:
        orm_mode = True


from datetime import datetime

class EvidencijaBase(BaseModel):
    vrsta_pristupa: str

class EvidencijaCreate(EvidencijaBase):
    korisnik_id: int
    karton_id: int

class EvidencijaOut(EvidencijaBase):
    evidencija_id: int
    korisnik_id: int
    karton_id: int
    vrijeme_pristupa: datetime

class DijagnozaUpdate(BaseModel):
    opis_dijagnoze: str
    datum_dijagnoze: date


    class Config:
        from_attributes = True  # Pydantic v2



# ───── TERMIN ─────
class TerminBase(BaseModel):
    datum_vrijeme: datetime
    status_termina: str
    razlog_pregleda: Optional[str] = None


class TerminCreate(TerminBase):
    pacijent_id: int
    lijecnik_id: int


class TerminOut(TerminBase):
    termin_id: int
    pacijent_id: int
    lijecnik_id: int

    class Config:
        orm_mode = True

class KartonOut(BaseModel):
    karton_id: int
    pacijent_id: int
    datum_otvaranja: date
    status_aktivnosti: str

    class Config:
        orm_mode = True

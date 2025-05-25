from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Pacijent(Base):
    __tablename__ = "pacijent"

    pacijent_id = Column(Integer, primary_key=True, index=True)
    oib = Column(String(11), unique=True, nullable=False)
    ime = Column(String(50), nullable=False)
    prezime = Column(String(50), nullable=False)
    kontakt = Column(String(50))

    kartoni = relationship("Karton", back_populates="pacijent")
    termini = relationship("Termin", back_populates="pacijent")


class Karton(Base):
    __tablename__ = "karton"

    karton_id = Column(Integer, primary_key=True, index=True)
    pacijent_id = Column(Integer, ForeignKey("pacijent.pacijent_id"), nullable=False)
    datum_otvaranja = Column(Date, nullable=False)
    status_aktivnosti = Column(String(20), nullable=False)

    pacijent = relationship("Pacijent", back_populates="kartoni")
    dijagnoze = relationship("Dijagnoza", back_populates="karton")
    pristupi = relationship("EvidencijaPristupa", back_populates="karton")


class Korisnik(Base):
    __tablename__ = "korisnik"

    korisnik_id = Column(Integer, primary_key=True, index=True)
    korisnicko_ime = Column(String(50), unique=True, nullable=False)
    lozinka = Column(String(100), nullable=False)
    ime = Column(String(50))
    prezime = Column(String(50))
    uloga = Column(String(30), nullable=False)

    dijagnoze = relationship("Dijagnoza", back_populates="lijecnik")
    terapije = relationship("Terapija", back_populates="lijecnik")
    pristupi = relationship("EvidencijaPristupa", back_populates="korisnik")
    termini = relationship("Termin", back_populates="lijecnik")


class Dijagnoza(Base):
    __tablename__ = "dijagnoza"

    dijagnoza_id = Column(Integer, primary_key=True, index=True)
    karton_id = Column(Integer, ForeignKey("karton.karton_id"), nullable=False)
    lijecnik_id = Column(Integer, ForeignKey("korisnik.korisnik_id"), nullable=False)
    opis_dijagnoze = Column(Text, nullable=False)
    datum_dijagnoze = Column(Date, nullable=False)

    karton = relationship("Karton", back_populates="dijagnoze")
    lijecnik = relationship("Korisnik", back_populates="dijagnoze")
    terapije = relationship("Terapija", back_populates="dijagnoza")


class Terapija(Base):
    __tablename__ = "terapija"

    terapija_id = Column(Integer, primary_key=True, index=True)
    dijagnoza_id = Column(Integer, ForeignKey("dijagnoza.dijagnoza_id"), nullable=False)
    lijecnik_id = Column(Integer, ForeignKey("korisnik.korisnik_id"), nullable=False)
    opis_terapije = Column(Text, nullable=False)

    dijagnoza = relationship("Dijagnoza", back_populates="terapije")
    lijecnik = relationship("Korisnik", back_populates="terapije")


class EvidencijaPristupa(Base):
    __tablename__ = "evidencija_pristupa"

    evidencija_id = Column(Integer, primary_key=True, index=True)
    korisnik_id = Column(Integer, ForeignKey("korisnik.korisnik_id"), nullable=False)
    karton_id = Column(Integer, ForeignKey("karton.karton_id"), nullable=False)
    vrsta_pristupa = Column(String(50), nullable=False)
    vrijeme_pristupa = Column(TIMESTAMP, nullable=False, server_default=func.now())

    korisnik = relationship("Korisnik", back_populates="pristupi")
    karton = relationship("Karton", back_populates="pristupi")


class Termin(Base):
    __tablename__ = "termin"

    termin_id = Column(Integer, primary_key=True, index=True)
    pacijent_id = Column(Integer, ForeignKey("pacijent.pacijent_id"), nullable=False)
    lijecnik_id = Column(Integer, ForeignKey("korisnik.korisnik_id"), nullable=False)
    datum_vrijeme = Column(TIMESTAMP, nullable=False)
    status_termina = Column(String(50), nullable=False)
    razlog_pregleda = Column(String(255))

    pacijent = relationship("Pacijent", back_populates="termini")
    lijecnik = relationship("Korisnik", back_populates="termini")

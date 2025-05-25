# backend/main.py

from fastapi import FastAPI
from routers import patients
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router, prefix="/patients", tags=["Patients"])

@app.get("/")
def root():
    return {"message": "Hello from DIGKAR backend"}

from routers import patients, users, kartoni  # add kartoni

app.include_router(kartoni.router, prefix="/kartoni", tags=["Kartoni"])

from routers import dijagnoze
app.include_router(dijagnoze.router, prefix="/dijagnoze", tags=["Dijagnoze"])

from routers import terapije
app.include_router(terapije.router, prefix="/terapije", tags=["Terapije"])

from fastapi import FastAPI
from routers import users


app.include_router(users.router, prefix="/users", tags=["Users"])

from routers import termini
app.include_router(termini.router, prefix="/termini", tags=["Termini"])

from routers import evidencija
app.include_router(evidencija.router, prefix="/evidencija", tags=["Evidencija pristupa"])

from routers import users
app.include_router(users.router, prefix="/korisnici", tags=["Korisnici"])

from routers import kartoni

app.include_router(kartoni.router, prefix="/kartoni", tags=["Kartoni"])

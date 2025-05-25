# backend/main.py

from fastapi import FastAPI
from routers import patients
from fastapi.middleware.cors import CORSMiddleware
from routers import patients, users, kartoni 
from routers import dijagnoze
from routers import terapije
from routers import users
from routers import termini
from routers import evidencija


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


app.include_router(kartoni.router, prefix="/kartoni", tags=["Kartoni"])


app.include_router(dijagnoze.router, prefix="/dijagnoze", tags=["Dijagnoze"])

from routers import terapije
app.include_router(terapije.router, prefix="/terapije", tags=["Terapije"])

from fastapi import FastAPI
from routers import users


app.include_router(users.router, prefix="/users", tags=["Users"])


app.include_router(termini.router, prefix="/termini", tags=["Termini"])


app.include_router(evidencija.router, prefix="/evidencija", tags=["Evidencija pristupa"])


app.include_router(users.router, prefix="/korisnici", tags=["Korisnici"])



app.include_router(kartoni.router, prefix="/kartoni", tags=["Kartoni"])

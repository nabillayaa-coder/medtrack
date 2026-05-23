from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.database import engine
from app import models
from app.routes import auth, medications

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MedTrack")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(medications.router)


@app.get("/")
def root():
    return RedirectResponse(url="/dashboard")
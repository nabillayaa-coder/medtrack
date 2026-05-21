from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.database import engine
from app import models
from app.routes import auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MedTrack")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router)


@app.get("/")
def root():
    return RedirectResponse(url="/login")


@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
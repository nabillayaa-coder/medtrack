from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, auth

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user = auth.require_login(request, db)
    if isinstance(user, RedirectResponse):
        return user

    medications = db.query(models.Medication).filter(
        models.Medication.user_id == user.id,
        models.Medication.is_active == True
    ).order_by(models.Medication.created_at.desc()).all()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "medications": medications,
    })


@router.get("/medications/add", response_class=HTMLResponse)
def add_medication_page(request: Request, db: Session = Depends(get_db)):
    user = auth.require_login(request, db)
    if isinstance(user, RedirectResponse):
        return user
    return templates.TemplateResponse("add_medication.html", {"request": request, "user": user})


@router.post("/medications/add")
def add_medication(
    request: Request,
    name: str = Form(...),
    dosage: str = Form(...),
    frequency: str = Form(...),
    notes: str = Form(""),
    db: Session = Depends(get_db),
):
    user = auth.require_login(request, db)
    if isinstance(user, RedirectResponse):
        return user

    med = models.Medication(
        name=name,
        dosage=dosage,
        frequency=frequency,
        notes=notes or None,
        user_id=user.id,
    )
    db.add(med)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=302)


@router.post("/medications/{med_id}/delete")
def delete_medication(med_id: int, request: Request, db: Session = Depends(get_db)):
    user = auth.require_login(request, db)
    if isinstance(user, RedirectResponse):
        return user

    med = db.query(models.Medication).filter(
        models.Medication.id == med_id,
        models.Medication.user_id == user.id
    ).first()
    if med:
        med.is_active = False
        db.commit()
    return RedirectResponse(url="/dashboard", status_code=302)
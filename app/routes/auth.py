from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, auth

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request, "error": None})


@router.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    if db.query(models.User).filter(models.User.email == email).first():
        return templates.TemplateResponse("auth/register.html", {
            "request": request, "error": "Email already registered."
        })
    if db.query(models.User).filter(models.User.username == username).first():
        return templates.TemplateResponse("auth/register.html", {
            "request": request, "error": "Username already taken."
        })
    user = models.User(
        username=username,
        email=email,
        hashed_password=auth.hash_password(password),
    )
    db.add(user)
    db.commit()
    return RedirectResponse(url="/login?registered=1", status_code=302)


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, registered: str = None):
    return templates.TemplateResponse("auth/login.html", {
        "request": request,
        "error": None,
        "success": "Account created! Please log in." if registered else None
    })


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not auth.verify_password(password, user.hashed_password):
        return templates.TemplateResponse("auth/login.html", {
            "request": request, "error": "Invalid email or password.", "success": None
        })
    token = auth.create_access_token({"sub": user.email})
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=60*60*24*7)
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")
    return response
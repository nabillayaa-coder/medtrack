# MedTrack

![Python](https://img.shields.io/badge/Python-3.11-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.103-green) ![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)

MedTrack is a full-stack medication tracking web application built to help users manage their daily medications, track doses, and stay consistent with their treatment plans.

---

## Features

- User registration and login with JWT authentication
- Add, view and delete medications
- Track dosage and frequency per medication
- Clean and responsive UI
- Secure cookie-based sessions

---

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite

### Frontend
- Jinja2 Templates
- Custom CSS

### Auth
- JWT (python-jose)
- Bcrypt password hashing

### Tools
- Git / GitHub
- Uvicorn

---

## Project Structure
medtrack/
├── app/
│   ├── routes/
│   │   ├── auth.py
│   │   └── medications.py
│   ├── templates/
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   └── add_medication.html
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── auth.py
│   ├── database.py
│   ├── main.py
│   └── models.py
├── .env.example
├── requirements.txt
├── Procfile
└── README.md

---

## Installation

```bash
git clone https://github.com/nabillayaa-coder/medtrack.git
cd medtrack
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Open http://localhost:8000

---

## Roadmap

- [x] User auth
- [x] Add / view / delete medications
- [x] Navbar and UI
- [ ] Mark dose as taken
- [ ] Dose history log
- [ ] Adherence stats
- [ ] Edit medications
- [ ] Search and filter
- [ ] Profile page
- [ ] Deploy on Render
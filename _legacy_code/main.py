from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import uvicorn
import os

from database import SessionLocal, engine
from models import Base, Candidate
from ml_engine import RetentionModel

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Xon-Intake | Neural Executive Interview")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

model = RetentionModel()

# Questions
QUESTIONS = [
    "What capability are you building that creates enterprise leverage?",
    "Describe a decision you made without full data.",
    "Tell me about a professional failure and what changed.",
    "How do you handle prolonged stress under pressure?",
    "What would your first 30-day impact strategy be?"
]


def score_response(text: str):
    words = len(text.split())
    clarity = min(words / 10, 10)
    depth = min(words / 15, 10)
    ownership = 8 if "I" in text else 4
    return clarity, depth, ownership


@app.get("/", response_class=HTMLResponse)
def interview_page(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "questions": QUESTIONS
    })


@app.post("/submit")
def submit_interview(
    request: Request,
    q1: str = Form(...),
    q2: str = Form(...),
    q3: str = Form(...),
    q4: str = Form(...),
    q5: str = Form(...)
):
    db: Session = SessionLocal()

    responses = [q1, q2, q3, q4, q5]

    clarity_total = 0
    depth_total = 0
    ownership_total = 0

    for r in responses:
        clarity, depth, ownership = score_response(r)
        clarity_total += clarity
        depth_total += depth
        ownership_total += ownership

    clarity_avg = clarity_total / 5
    depth_avg = depth_total / 5
    ownership_avg = ownership_total / 5

    retention = model.predict([
        clarity_avg,
        depth_avg,
        ownership_avg
    ])

    candidate = Candidate(
        clarity=clarity_avg,
        depth=depth_avg,
        ownership=ownership_avg,
        retention_prediction=retention
    )

    db.add(candidate)
    db.commit()
    db.close()

    return RedirectResponse(url="/dashboard", status_code=303)


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    db: Session = SessionLocal()
    candidates = db.query(Candidate).all()
    db.close()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "candidates": candidates
    })


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
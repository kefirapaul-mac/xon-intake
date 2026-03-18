from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import uuid

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

SESSION_STORE = {}

def generate_ai_interpretation(name, role):
    return {
        "candidate": name,
        "role": role,
        "baseline": "Stable initial presentation",
        "adaptive_pattern": "Moderate cognitive load under evaluative prompts",
        "communication_style": "Structured verbal processing",
        "stress_response": "Mild anticipatory tension with recovery",
        "neural_user_manual": "Candidate responds better to structured expectations and written follow-up.",
        "ai_score": 82
    }

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard-page", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/result-page", response_class=HTMLResponse)
async def result_page(request: Request):
    return templates.TemplateResponse("result.html", {"request": request})

@app.post("/start-session")
async def start_session(
    name: str = Form(...),
    age: int = Form(...),
    sex: str = Form(...),
    role: str = Form(...),
    experience: str = Form(...)
):
    session_id = str(uuid.uuid4())
    ai_result = generate_ai_interpretation(name, role)

    SESSION_STORE[session_id] = {
        "session_id": session_id,
        "timestamp": str(datetime.now()),
        "candidate": {
            "name": name,
            "age": age,
            "sex": sex,
            "role": role,
            "experience": experience
        },
        "ai_analysis": ai_result,
        "hr_score": None,
        "therapist_score": None,
        "combined_score": None
    }

    return JSONResponse({
        "session_id": session_id,
        "ai_analysis": ai_result
    })

@app.get("/dashboard")
async def dashboard():
    if not SESSION_STORE:
        return {"error": "No session data"}

    latest = list(SESSION_STORE.values())[-1]
    return latest

@app.post("/submit-score")
async def submit_score(
    session_id: str = Form(...),
    hr_score: int = Form(...),
    therapist_score: int = Form(...)
):
    session = SESSION_STORE.get(session_id)

    if not session:
        return {"error": "Invalid session"}

    ai_score = session["ai_analysis"]["ai_score"]
    combined = round((ai_score + hr_score + therapist_score) / 3, 2)

    session["hr_score"] = hr_score
    session["therapist_score"] = therapist_score
    session["combined_score"] = combined

    return {
        "combined_score": combined
    }

@app.get("/candidate-result")
async def candidate_result():
    if not SESSION_STORE:
        return {"error": "No result"}

    latest = list(SESSION_STORE.values())[-1]

    return {
        "overall_score": latest["combined_score"]
    }
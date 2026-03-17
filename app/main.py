from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import uuid

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ------------------------------
# In-memory session store
# ------------------------------

SESSION_STORE = {}

# ------------------------------
# Smart scoring helper
# ------------------------------

def generate_ai_interpretation(name, role):
    return {
        "candidate": name,
        "role": role,
        "baseline": "Stable initial presentation",
        "adaptive_pattern": "Moderate cognitive load under evaluative prompts",
        "communication_style": "Structured verbal processing",
        "stress_response": "Mild anticipatory tension with recovery",
        "neural_user_manual": (
            "Candidate responds better to structured expectations, "
            "written follow-up, and predictable task framing."
        ),
        "ai_score": 82
    }

# ------------------------------
# Home
# ------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ------------------------------
# Start candidate intake
# ------------------------------

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
        "message": "Session created",
        "session_id": session_id,
        "ai_analysis": ai_result
    })

# ------------------------------
# Dashboard
# ------------------------------

@app.get("/dashboard")
async def dashboard():
    if not SESSION_STORE:
        return {
            "dashboard": {
                "error": "No session data"
            },
            "anomaly_analysis": {
                "anomaly_score": 0,
                "pattern": "Insufficient data"
            }
        }

    latest_session = list(SESSION_STORE.values())[-1]

    return {
        "dashboard": latest_session,
        "anomaly_analysis": {
            "anomaly_score": 18,
            "pattern": "Baseline stable with adaptive variation"
        }
    }

# ------------------------------
# Recruiter scoring
# ------------------------------

@app.post("/submit-human-score")
async def submit_human_score(
    session_id: str = Form(...),
    hr_score: int = Form(...),
    therapist_score: int = Form(...)
):
    if session_id not in SESSION_STORE:
        return {"error": "Invalid session"}

    ai_score = SESSION_STORE[session_id]["ai_analysis"]["ai_score"]

    combined = round((ai_score + hr_score + therapist_score) / 3, 2)

    SESSION_STORE[session_id]["hr_score"] = hr_score
    SESSION_STORE[session_id]["therapist_score"] = therapist_score
    SESSION_STORE[session_id]["combined_score"] = combined

    return {
        "session_id": session_id,
        "combined_score": combined
    }
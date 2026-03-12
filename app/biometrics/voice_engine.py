import os
import uuid
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
templates = Jinja2Templates(directory=TEMPLATE_DIR)

# =========================================================
# CORE PSYCHOLOGICAL SCORING ENGINE
# =========================================================

def compute_psychological_profile(face_metrics: dict, voice_metrics: dict):

    stress_score = 0
    confidence_score = 100
    emotional_stability = 100
    cognitive_load = 0

    # FACE SIGNALS
    if face_metrics:
        if face_metrics.get("brow_tension", 0) > 0.03:
            stress_score += 20

        if face_metrics.get("mouth_tension", 0) > 0.02:
            stress_score += 15

        if face_metrics.get("eye_openness", 1) < 0.01:
            stress_score += 15

        if face_metrics.get("blink_rate", 0) > 35:
            stress_score += 10
            cognitive_load += 20

    # VOICE SIGNALS
    if voice_metrics:
        if voice_metrics.get("pitch_variation", 0) > 40:
            stress_score += 20
            cognitive_load += 20

        if voice_metrics.get("pause_frequency", 0) > 0.4:
            stress_score += 10
            cognitive_load += 20

        if voice_metrics.get("speech_rate", 1) < 0.5:
            emotional_stability -= 15

    confidence_score = max(0, 100 - stress_score)
    emotional_stability = max(0, emotional_stability - (stress_score // 2))
    behavioral_risk = min(100, stress_score + (100 - confidence_score))

    if stress_score < 30:
        classification = "Calm / Composed"
        risk_label = "Low Behavioral Risk"
    elif stress_score < 60:
        classification = "Mild Cognitive Load"
        risk_label = "Moderate Risk Pattern"
    elif stress_score < 85:
        classification = "Elevated Stress Response"
        risk_label = "High Volatility Indicator"
    else:
        classification = "Severe Stress Response"
        risk_label = "Critical Behavioral Risk"

    return {
        "stress_score": stress_score,
        "confidence_score": confidence_score,
        "emotional_stability": emotional_stability,
        "cognitive_load_index": cognitive_load,
        "behavioral_risk": behavioral_risk,
        "classification": classification,
        "risk_label": risk_label
    }

# =========================================================
# AI NARRATIVE ENGINE
# =========================================================

def generate_psychological_narrative(profile: dict):

    stress = profile["stress_score"]
    confidence = profile["confidence_score"]
    stability = profile["emotional_stability"]
    load = profile["cognitive_load_index"]

    narrative = f"""
Behavioral Interpretation Report:

The candidate presents with a stress index of {stress}/100, 
with a confidence stability score of {confidence}/100.

Observed emotional regulation capacity is estimated at {stability}/100, 
while cognitive processing load indicators suggest a load index of {load}/100.

Interpretation:

"""

    if stress < 30:
        narrative += """
The behavioral pattern indicates emotional composure, 
adaptive self-regulation, and stable executive functioning. 
No significant volatility markers detected.
"""
    elif stress < 60:
        narrative += """
The candidate demonstrates mild cognitive strain. 
This may reflect performance pressure rather than intrinsic instability. 
Emotional control remains functionally intact.
"""
    elif stress < 85:
        narrative += """
Elevated stress responses were detected. 
Markers suggest heightened sympathetic activation and potential 
decision-making rigidity under pressure.
Further situational evaluation recommended.
"""
    else:
        narrative += """
Severe stress markers observed. 
This profile indicates compromised emotional regulation and 
possible executive instability in high-pressure environments.
Comprehensive behavioral assessment advised.
"""

    return narrative.strip()

# =========================================================
# ROUTES
# =========================================================

@app.get("/", response_class=HTMLResponse)
async def intake_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit", response_class=HTMLResponse)
async def submit_candidate(
    request: Request,
    full_name: str = Form(...),
    email: str = Form(...),
    video: UploadFile = File(None),
    audio: UploadFile = File(None)
):

    if video:
        video_filename = f"{uuid.uuid4()}.mp4"
        with open(os.path.join(UPLOAD_DIR, video_filename), "wb") as f:
            f.write(await video.read())

    if audio:
        audio_filename = f"{uuid.uuid4()}.wav"
        with open(os.path.join(UPLOAD_DIR, audio_filename), "wb") as f:
            f.write(await audio.read())

    # Placeholder metrics (will be replaced by real analyzers later)
    face_metrics = {
        "brow_tension": 0.02,
        "mouth_tension": 0.01,
        "eye_openness": 0.02,
        "blink_rate": 28
    }

    voice_metrics = {
        "pitch_variation": 35,
        "pause_frequency": 0.3,
        "speech_rate": 0.7
    }

    profile = compute_psychological_profile(face_metrics, voice_metrics)
    narrative = generate_psychological_narrative(profile)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "name": full_name,
            "email": email,
            "profile": profile,
            "narrative": narrative
        }
    )
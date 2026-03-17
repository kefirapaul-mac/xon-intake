from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json

from app.biometric_engine import (
    process_metrics,
    set_question_intensity,
    get_session_data
)
from app.anomaly_engine import detect_behavioral_anomalies
from app.analytics import generate_recruiter_dashboard

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            if "question_level" in payload:
                set_question_intensity(payload["question_level"])
                continue

            if "metrics" in payload:
                metrics = process_metrics(
                    payload["stress"],
                    payload["deception"],
                    payload["engagement"],
                    payload["voice"]
                )
                await websocket.send_text(json.dumps(metrics))

    except:
        pass


@app.get("/dashboard")
def recruiter_dashboard():
    data = get_session_data()
    dashboard = generate_recruiter_dashboard(data)
    anomaly = detect_behavioral_anomalies(data)

    return JSONResponse({
        "dashboard": dashboard,
        "anomaly_analysis": anomaly
    })


@app.get("/health")
def health():
    return {"status": "xon live"}
import numpy as np

def detect_behavioral_anomalies(session_data):
    if len(session_data) < 30:
        return {"anomaly_score": 0, "pattern": "Insufficient data"}

    stress_values = [d["stress"] for d in session_data]
    voice_values = [d["voice"] for d in session_data]

    stress_std = np.std(stress_values)
    voice_std = np.std(voice_values)

    anomaly_score = int((stress_std + voice_std) * 2)
    anomaly_score = min(100, anomaly_score)

    if anomaly_score > 60:
        pattern = "High volatility detected"
    elif anomaly_score > 30:
        pattern = "Moderate emotional fluctuation"
    else:
        pattern = "Stable behavioral pattern"

    return {
        "anomaly_score": anomaly_score,
        "pattern": pattern
    }
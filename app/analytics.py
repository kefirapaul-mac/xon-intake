import numpy as np

def generate_recruiter_dashboard(session_data):
    if not session_data:
        return {"error": "No session data"}

    avg_stress = int(np.mean([d["stress"] for d in session_data]))
    avg_deception = int(np.mean([d["deception"] for d in session_data]))
    avg_engagement = int(np.mean([d["engagement"] for d in session_data]))
    avg_voice = int(np.mean([d["voice"] for d in session_data]))
    avg_stability = int(np.mean([d["stability"] for d in session_data]))

    hiring_recommendation = "RECOMMENDED" if avg_stability > 65 else "REVIEW"

    return {
        "avg_stress": avg_stress,
        "avg_deception": avg_deception,
        "avg_engagement": avg_engagement,
        "avg_voice": avg_voice,
        "stability_index": avg_stability,
        "recommendation": hiring_recommendation
    }
import numpy as np
from collections import deque

stress_buffer = deque(maxlen=500)
deception_buffer = deque(maxlen=500)
engagement_buffer = deque(maxlen=500)
voice_buffer = deque(maxlen=500)

session_data = []
question_intensity = 1


def set_question_intensity(level: int):
    global question_intensity
    question_intensity = level


def process_metrics(stress, deception, engagement, voice):
    stress_buffer.append(stress)
    deception_buffer.append(deception)
    engagement_buffer.append(engagement)
    voice_buffer.append(voice)

    avg_stress = int(np.mean(stress_buffer))
    avg_deception = int(np.mean(deception_buffer))
    avg_engagement = int(np.mean(engagement_buffer))
    avg_voice = int(np.mean(voice_buffer))

    contextual = avg_stress * question_intensity
    stability = 100 - int((contextual + avg_deception + avg_voice) / 3)
    stability = max(0, min(100, stability))

    session_data.append({
        "stress": avg_stress,
        "deception": avg_deception,
        "engagement": avg_engagement,
        "voice": avg_voice,
        "stability": stability
    })

    return {
        "stress": avg_stress,
        "deception": avg_deception,
        "engagement": avg_engagement,
        "voice": avg_voice,
        "csi": stability
    }


def get_session_data():
    return session_data
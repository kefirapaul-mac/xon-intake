import random

def compute_ai_score():
    facial_component = random.uniform(60, 95)
    vocal_component = random.uniform(55, 90)
    cognitive_load = random.uniform(65, 100)

    weighted_score = (
        facial_component * 0.3 +
        vocal_component * 0.3 +
        cognitive_load * 0.4
    )

    return round(weighted_score, 2)

def detect_behavior_flags():
    """
    Simulated behavioral flag engine.
    Later replaced with real micro-expression + NLP detection.
    """

    red_flags = random.randint(0, 3)
    green_flags = random.randint(0, 2)

    return red_flags, green_flags
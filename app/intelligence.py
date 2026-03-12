import math
import random
from datetime import datetime


# ===============================
# CORE PSYCHOLOGICAL ENGINE
# Hybrid Clinical + Executive AI
# ===============================

def normalize(value, min_val=0, max_val=100):
    return max(min_val, min(max_val, value))


def calculate_emotional_stability(stress_score, sleep_hours):
    base = 70 - (stress_score * 0.6)
    sleep_bonus = (sleep_hours - 6) * 5
    return normalize(base + sleep_bonus)


def calculate_cognitive_flexibility(openness_score, problem_solving_score):
    score = (openness_score * 0.6) + (problem_solving_score * 0.4)
    return normalize(score)


def calculate_dominance(assertiveness, leadership_index):
    score = (assertiveness * 0.7) + (leadership_index * 0.3)
    return normalize(score)


def calculate_impulse_regulation(impulsivity, emotional_reactivity):
    score = 100 - ((impulsivity * 0.6) + (emotional_reactivity * 0.4))
    return normalize(score)


def calculate_burnout_risk(stress_score, workload_hours):
    risk = (stress_score * 0.7) + (workload_hours * 0.3)
    return normalize(risk)


def calculate_deception_index(response_consistency, hesitation_score):
    score = (100 - response_consistency) * 0.5 + hesitation_score * 0.5
    return normalize(score)


def behavioral_consistency(random_variance):
    score = 100 - random_variance
    return normalize(score)


# ===============================
# EXPERIMENTAL DARK AI LAYER
# ===============================

def anomaly_detection(profile):
    values = list(profile.values())
    variance = sum([(v - sum(values)/len(values))**2 for v in values]) / len(values)
    return normalize(variance / 10)


def executive_pressure_index(dominance, burnout_risk):
    return normalize((dominance * 0.6) + (burnout_risk * 0.4))


# ===============================
# MASTER ENGINE
# ===============================

def compute_psychological_profile(form_data):

    # Simulated biometric signals (safe scaffold)
    biometric_hesitation = random.randint(10, 40)
    micro_expression_variance = random.randint(5, 25)

    stress_score = int(form_data.get("stress_score", 50))
    sleep_hours = int(form_data.get("sleep_hours", 6))
    openness_score = int(form_data.get("openness_score", 50))
    problem_solving_score = int(form_data.get("problem_solving_score", 50))
    assertiveness = int(form_data.get("assertiveness", 50))
    leadership_index = int(form_data.get("leadership_index", 50))
    impulsivity = int(form_data.get("impulsivity", 50))
    emotional_reactivity = int(form_data.get("emotional_reactivity", 50))
    workload_hours = int(form_data.get("workload_hours", 40))
    response_consistency = int(form_data.get("response_consistency", 80))

    emotional_stability = calculate_emotional_stability(stress_score, sleep_hours)
    cognitive_flexibility = calculate_cognitive_flexibility(openness_score, problem_solving_score)
    dominance = calculate_dominance(assertiveness, leadership_index)
    impulse_regulation = calculate_impulse_regulation(impulsivity, emotional_reactivity)
    burnout_risk = calculate_burnout_risk(stress_score, workload_hours)
    deception_index = calculate_deception_index(response_consistency, biometric_hesitation)
    consistency = behavioral_consistency(micro_expression_variance)

    profile = {
        "Emotional Stability": emotional_stability,
        "Cognitive Flexibility": cognitive_flexibility,
        "Dominance": dominance,
        "Impulse Regulation": impulse_regulation,
        "Burnout Risk": burnout_risk,
        "Deception Index": deception_index,
        "Behavioral Consistency": consistency,
    }

    anomaly_score = anomaly_detection(profile)
    pressure_index = executive_pressure_index(dominance, burnout_risk)

    profile["Anomaly Index"] = anomaly_score
    profile["Executive Pressure Index"] = pressure_index
    profile["Timestamp"] = datetime.utcnow().isoformat()

    return profile
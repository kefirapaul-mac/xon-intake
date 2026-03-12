import random


def compute_psychological_profile(candidate):

    # --- Simulated biometric extraction ---
    # (Later this will connect to real voice + facial engines)

    stress_level = random.randint(30, 85)
    cognitive_load = random.randint(25, 90)
    confidence_score = random.randint(40, 95)

    # --- Derived Intelligence Metrics ---

    behavioral_volatility = int(
        (stress_level * 0.5) +
        (cognitive_load * 0.3) -
        (confidence_score * 0.2)
    )

    pressure_tolerance = int(
        (confidence_score * 0.6) -
        (stress_level * 0.3)
    )

    adaptability_score = int(
        (100 - cognitive_load) * 0.5 +
        confidence_score * 0.5
    )

    # Normalize bounds
    behavioral_volatility = max(0, min(100, behavioral_volatility))
    pressure_tolerance = max(0, min(100, pressure_tolerance))
    adaptability_score = max(0, min(100, adaptability_score))

    # --- Risk Classification Logic ---

    if behavioral_volatility > 70 or pressure_tolerance < 30:
        risk_classification = "High"
    elif behavioral_volatility > 45:
        risk_classification = "Moderate"
    else:
        risk_classification = "Low"

    # --- Narrative Generation ---

    narrative = generate_narrative(
        stress_level,
        cognitive_load,
        confidence_score,
        behavioral_volatility,
        pressure_tolerance,
        adaptability_score
    )

    return {
        "stress_level": stress_level,
        "cognitive_load": cognitive_load,
        "confidence_score": confidence_score,
        "behavioral_volatility": behavioral_volatility,
        "pressure_tolerance": pressure_tolerance,
        "adaptability_score": adaptability_score,
        "risk_classification": risk_classification,
        "narrative": narrative
    }


def generate_narrative(stress, load, confidence, volatility, pressure, adaptability):

    summary = []

    if stress > 70:
        summary.append("Elevated physiological stress markers detected.")
    else:
        summary.append("Stress markers remain within controlled parameters.")

    if load > 70:
        summary.append("High cognitive processing load observed.")
    else:
        summary.append("Cognitive load appears stable and manageable.")

    if confidence > 75:
        summary.append("Strong outward confidence indicators present.")
    else:
        summary.append("Confidence signals are moderate or situational.")

    if pressure < 35:
        summary.append("Pressure tolerance may decline under executive stress.")
    else:
        summary.append("Subject likely maintains composure under pressure.")

    if volatility > 65:
        summary.append("Behavioral volatility suggests emotional fluctuation risk.")
    else:
        summary.append("Behavioral responses appear consistent and regulated.")

    if adaptability > 70:
        summary.append("High adaptability potential detected.")
    else:
        summary.append("Adaptability range is moderate.")

    return " ".join(summary)
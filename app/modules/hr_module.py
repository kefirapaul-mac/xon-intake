def validate_hr_score(score: float) -> float:
    if score < 0 or score > 100:
        raise ValueError("HR score must be between 0 and 100")
    return score
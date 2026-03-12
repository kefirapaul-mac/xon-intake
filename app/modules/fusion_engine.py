def compute_combined_score(hr_score, therapist_score, ai_score,
                           red_flags: int = 0,
                           green_flags: int = 0):
    """
    Advanced Fusion Logic

    - Base weighted score
    - Penalize red flags
    - Reward green flags
    """

    # Weighted fusion
    base_score = (
        hr_score * 0.3 +
        therapist_score * 0.3 +
        ai_score * 0.4
    )

    # Red flag penalty (each red flag reduces 2%)
    penalty = red_flags * 2

    # Green flag bonus (each green adds 1%)
    bonus = green_flags * 1

    final_score = base_score - penalty + bonus

    # Bound between 0 and 100
    final_score = max(0, min(100, final_score))

    return round(final_score, 2)
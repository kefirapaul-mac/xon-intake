from app.security.encryption import encrypt_value, decrypt_value

def store_therapist_score(score: float) -> str:
    return encrypt_value(score)

def retrieve_therapist_score(token: str) -> float:
    return decrypt_value(token)
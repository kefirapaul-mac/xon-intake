from cryptography.fernet import Fernet

SECRET_KEY = Fernet.generate_key()
cipher = Fernet(SECRET_KEY)

def encrypt_value(value: float) -> str:
    return cipher.encrypt(str(value).encode()).decode()

def decrypt_value(token: str) -> float:
    return float(cipher.decrypt(token.encode()).decode())
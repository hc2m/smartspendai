import hashlib

def hash_otp(otp: str):
    return hashlib.sha256(otp.encode()).hexdigest()
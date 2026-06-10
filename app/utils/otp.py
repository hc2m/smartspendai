import secrets


# This generates 6 digit otp 
def generate_otp():
    return str(secrets.randbelow(900000) + 100000)
from pydantic import BaseModel

class ForgotPasswordRequest(BaseModel):
    email: str
    
class VerifyOtpRequest(BaseModel):
    email: str
    otp: str

class ResetPasswordRequest(BaseModel):
    new_password: str
    reset_token: str
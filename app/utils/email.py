import smtplib
from email.mime.text import MIMEText

import os

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")

def send_otp_email(to_email, otp):
    html = f"""
    <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>Your OTP code is:</p>
            <h1>{otp}</h1>
            <p>This code will expire in <b>5 minutes</b>.</p>
            <br>
            <p>If you did not request this, please ignore this email.</p>
            <p>SmartSpend AI Security Team</p>
            <strong>developed by HC2M team</strong>
        </body>
    </html>
    """
    msg = MIMEText(html,"html")
    msg["Subject"] = "SmartSpend AI - Password Reset OTP"
    msg["From"] = EMAIL
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(EMAIL,APP_PASSWORD)
    server.send_message(msg)
    server.quit()
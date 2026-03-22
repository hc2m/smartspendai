from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import os

EMAIL = os.getenv("EMAIL")
API_KEY = os.getenv("SENDGRID_API_KEY")

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

    try:
        message = Mail(
            from_email=EMAIL,
            to_emails=to_email,
            subject="Password Reset OTP",
            html_content=html
        )

        sg = SendGridAPIClient(api_key=API_KEY)
        response = sg.send(message=message)

        print("Email sent: ", response.status_code)
    except Exception as e:
        print("Email error: ", str(e))
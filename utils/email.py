import smtplib
from credentials import *
from email.message import EmailMessage


def send_email(receiver_email_id: str, message: str):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login(SENDER_ACCOUNT_ID, SENDER_ACCOUNT_APP_PASSWORD)
    print(f'message: {message}')
    # Set email content
    msg = EmailMessage()
    msg['Subject'] = 'AI RAG agent appointment'
    msg['From'] = SENDER_ACCOUNT_ID
    msg['To'] = RECEIVER_ACCOUNT_ID
    msg.set_content(message)
    # Send email
    s.send_message(msg)
    # terminating the session
    s.quit()

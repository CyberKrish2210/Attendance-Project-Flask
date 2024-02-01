import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
def send_email_function(subject, body, to_email):
    sender_email = "yashpadale108@gmail.com"
    app_password = "galh orgc thll wqbj"
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, to_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()
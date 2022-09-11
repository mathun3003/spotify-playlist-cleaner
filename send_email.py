import smtplib
import os
from dotenv import load_dotenv
load_dotenv()


def send_email(logs: str):
    user = os.getenv('SMTP_USER')
    pwd = os.getenv('SMTP_PASSWORD')
    # set subject and mail text
    subject = 'Monthly Report on your Spotify Playlist'
    mail_text = f"""
    Your Spotify Playlist has been updated:
    
    {logs}
    """
    # set email settings
    MAIL_FROM = user
    RCPT_TO = user
    MSG = 'From:%s\nTo:%s\nSubject:%s\n\n%s' % (MAIL_FROM, RCPT_TO, subject, mail_text)
    # connect and send email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(user, pwd)
    server.sendmail(MAIL_FROM, RCPT_TO, MSG)
    server.quit()
    pass

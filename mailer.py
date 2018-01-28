import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(user, pwd, recipient, subject, body):
    """
    Source https://stackoverflow.com/questions/882712/sending-html-email-using-python
    """

    me = user
    you = recipient

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    # text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = body

    # Record the MIME types of both parts - text/plain and text/html.
    part2 = MIMEText(html.encode('utf-8'), 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part2)
    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login(user, pwd)
    mail.sendmail(me, you, msg.as_string())
    mail.quit()
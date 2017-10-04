"""
These are email-related utilites.

"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import platform


def send_email(**kwargs):
    """
    Send an email, optionally with one or more attachments.
    Keywor args are:
    "to" : recipient
    "sender" : sending email
    "subject" : subject line of email
    "attachments" : list of dictionaries for attachments; each dict must have:
        "mimetype" : mimetype of attachment
        "data" : data for attachment
        "filename" : filename for attachment
    """
    recipient = kwargs.get("to")
    sender = kwargs.get("sender", "noreply@" + platform.node())
    msg = MIMEMultipart('alternative')
    msg['Subject'] = kwargs.get("subject")
    msg['To'] = recipient
    msg['From'] = sender

    message = MIMEText(kwargs.get("message"), 'plain')
    msg.attach(message)

    if kwargs.get('attachments'):
        for attachment in kwargs.get('attachments'):
            mimetype = attachment.get('mimetype', 'text/plain')
            part = MIMEBase(*mimetype.split("/"))
            part.set_payload(attachment.get("data"))
            encode_base64(part)
            part.add_header(
                "Content-Disposition",
                "attachment",
                filename=attachment.get("filename")
            )
            msg.attach(part)

    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(sender, recipient, msg.as_string())
    smtp.close()

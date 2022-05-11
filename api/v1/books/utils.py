import inspect
import random
import string
import threading

from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse
from django.template import loader
from django.template.defaultfilters import slugify

def sendMail(email_data):
    for key, value in email_data.items():
        if key == "subject":
            subject = value
        elif key == "message":
            message = value
        elif key == "recipient":
            recipient = value
        elif key == "reset_link":
            reset_link = value
        elif key == "username":
            username = value
    try:
        # email = EmailMessage(
        #     subject, message, from_email="noreply@doken.app", to=[recipient])

        html_message = loader.render_to_string(
            "email.html",
            {
                "reset_link": reset_link,
                "username": username,
                "subject": subject,
            },
        )
        email = EmailMessage(
            subject,
            html_message,
            from_email="noreply@doken.app",
            to=[recipient],
        )
        email.content_subtype = "html"
        return email

    except BadHeaderError:
        return HttpResponse("Invalid header found.")


class EmailThread(threading.Thread):
    def __init__(self, email_data):
        self.email_data = email_data
        threading.Thread.__init__(self)

    def run(self):
        self.email = sendMail(self.email_data)
        self.email.send(fail_silently=False)

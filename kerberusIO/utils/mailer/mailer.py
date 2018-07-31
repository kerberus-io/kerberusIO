from flask import render_template, url_for
from flask_mail import Mail, Message
from kerberusIO.application import app
import flask

import abc
from abc import ABC

mail = Mail(app)
default_sender = app.config["MAIL_DEFAULT_SENDER"]
default_template = ""
default_recipient = app.config["MAIL_DEFAULT_RECEIVER"]


def send_mail(recipient: str, subject: str, message: str, template: str=None, sender: str=None, reply_to: str=None):
    if not sender:
        sender = default_sender
    if not reply_to:
        reply_to = default_sender

    msg = Message(
        subject=subject,
        sender=sender,
        recipients=[recipient],
        reply_to=reply_to
    )

    if not template:
        template = default_template

    msg.body = message
    email = {"title": subject, "message": message}

    msg.html = render_template(template, email=email)


def send_contact(reply_to: str, subject: str, message: str):

    contact_msg = Message(
        'Form Email: {}'.format(subject),
        sender=default_sender,
        recipients=[default_recipient],
        reply_to=reply_to
    )

    contact_msg.body = message
    contact_msg.html = message

    mail.send(contact_msg)


# TODO: this need to be implemented
# TODO: This needs an actual form email to be sent out
def send_confirmation(reply_to: str, subject: str, message: str):

    contact_msg = Message(
        'Email Sent: {} - We got it and are looking into it'.format(subject),
        sender=default_sender,
        recipients=[reply_to],
        reply_to=default_sender
    )

    email = {"title": "Contact Confirm", "message": message}

    contact_msg.body = message
    contact_msg.html = render_template("email/confirmation_email.html", email=email)

    mail.send(contact_msg)

# TODO: make use of a message queue to speed up mailing.


if __name__ == '__main__':
    print(type(app))
    # with app.app_context():
        # send_contact('email@address.com', "test", "this is a test")

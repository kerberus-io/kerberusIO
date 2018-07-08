from flask import render_template, url_for
from flask_mail import Mail, Message
from kerberusIO.application import app

mail = Mail(app)
sender = app.config["MAIL_DEFAULT_SENDER"]


def send_contact(reply_to: str, subject: str, message):

    contact_msg = Message(
        'Form Email: {}'.format(subject),
        sender=sender,
        recipients=[''],
        reply_to=reply_to
    )

    contact_msg.body = message
    contact_msg.html = message

    mail.send(contact_msg)


# TODO: this need to be implemented
def send_confirmation(reply_to: str, subject: str, message):

    contact_msg = Message(
        'Form Email: {}'.format(subject),
        sender=sender,
        recipients=[''],
        reply_to=reply_to
    )

    contact_msg.body = message
    contact_msg.html = message

    mail.send(contact_msg)

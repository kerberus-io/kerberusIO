from flask import render_template, url_for
from flask_mail import Mail, Message
from kerberusIO.application import app

mail = Mail(app)

sender = ""


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

#
# if __name__ == '__main__':
#     send_confirmation("asouer@gmail.com", "test email", "this is a test")

from flask import render_template, redirect, request, url_for
from kerberusIO.application import app
from kerberusIO.utils.mailer import mailer


@app.route('/')
def main():
    phone = {"pretty": "(612) 555 - 5555", "link": "612-555-5555"}
    owners = [
        {"name": "Aaron Souer", "github": "asouer", "linkedin": "asouer"},
        {"name": "Lincoln Yellick", "github": "lyellick", "linkedin": "lincoln-hach-yellick-3867b088"}
    ]
    return render_template("index.html", owners=owners, phone=phone)


@app.route('/contact', methods=['POST'])
def contact():

    form = request.form
    mailer.send_confirmation(form["email"], form["subject"], form["message"])

    return redirect(url_for('dev'))

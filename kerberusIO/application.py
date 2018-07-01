from flask import Flask, render_template, redirect, url_for, request
import config


app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)

from kerberusIO.utils.mailer import mailer


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/updated')
def dev():
    owners = [
        {"name": "Aaron Souer"},
        {"name": "Lincoln Yellick"}
    ]
    return render_template("updated.html", owners=owners)


@app.route('/contact', methods=['POST'])
def contact():

    form = request.form
    mailer.send_confirmation(form["email"], form["subject"], form["message"])

    return redirect(url_for('dev'))


@app.route('/test_contact')
def test_contact():

    mailer.send_confirmation("asouer@gmail.com", "test", "123, testing")

    return redirect(url_for('dev'))


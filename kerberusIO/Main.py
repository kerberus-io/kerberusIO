from flask import render_template, redirect, request, url_for
from kerberusIO.application import app
from kerberusIO.utils.mailer import mailer


@app.route('/')
def main():
    # TODO: make dynamic

    phone = {"pretty": "(612) 555 - 5555", "link": "612-555-5555"}
    twitter = {"handle": "kerberusIO"}
    owners = [
        {"name": "Aaron Souer", "github": "asouer", "linkedin": "asouer"},
        {"name": "Lincoln Yellick", "github": "lyellick", "linkedin": "lincoln-hach-yellick-3867b088"}
    ]

    home = {"headline": "L337 Haxor Sites", "copy": "We make the best sites", "name": "home", "type": "splash"}
    about = {"headline": "Stuff and Things", "copy": "Thats what we do", "name": "about", "type": "splash"}
    services = {"headline": "Tech and Code", "copy": "Technobabble and Buzzwords", "name": "services", "type": "splash"}
    contact_page = {"phone": phone, "twitter": twitter, "owners": owners, "name": "contact", "type": "contact"}

    sections = [home, about, services, contact_page]

    return render_template("index.html", sections=sections)


@app.route('/contact', methods=['POST'])
def contact():

    form = request.form
    mailer.send_confirmation(form["email"], form["subject"], form["message"])

    return redirect(url_for('dev'))

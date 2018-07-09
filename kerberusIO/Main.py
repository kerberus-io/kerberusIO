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

    about = {"name": "about", "type": "split",
             "left": {"type": "list", "list":
                      ["Placeholder", "one", "two", "three", "four", "this needs to be styled better"]
                      },
             "right": {"type": "splash", "headline": "Things and Stuff", "copy": "We also do that!"}
             }

    services = {"name": "services", "type": "split",
                "right": {"type": "image", "file": "placeholder_card.png", "alt": "this is just a placeholder"},
                "left": {"type": "splash", "headline": "Tech and Code", "copy": "Technobabble and Buzzwords"}
                }

    contact_page = {"phone": phone, "twitter": twitter, "owners": owners, "name": "contact", "type": "contact"}

    sections = [home, about, services, contact_page]

    return render_template("index.html", sections=sections)


@app.route('/contact', methods=['POST'])
def contact():

    form = request.form
    mailer.send_contact(form["email"], form["subject"], form["message"])
    mailer.send_confirmation(form["email"], form["subject"], form["message"])

    return redirect(url_for('dev'))


@app.route('/test_confirm_email')
def test_confirm():

    email = {"title": "Test Confirm", "message": "This is a test email"}
    return render_template("email/confirmation_email.html", email=email)

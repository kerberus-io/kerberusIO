from flask import render_template, redirect, request, url_for, session
from config import Config
from kerberusIO.utils.db.users import Users
from kerberusIO.application import app
from kerberusIO.utils.mailer import mailer
from kerberusIO.utils.db.connection import SQLiteDB
from kerberusIO.utils.sessions.session import Session
from kerberusIO.models.Sections import *


db = SQLiteDB(Config)


@app.route('/')
def main():
    # TODO: make dynamic

    phone = {"pretty": "(612) 460 - 7063", "link": "612-460-7063"}
    twitter = {"handle": "kerberusIO"}
    owners = [
        {"name": "Aaron Souer", "github": "asouer", "linkedin": "asouer"},
        {"name": "Lincoln Yellick", "github": "lyellick", "linkedin": "lincoln-hach-yellick-3867b088"}
    ]

    home = {"headline": "kerberus.io", "copy": "freelance development", "name": "home",
            "type": "splash", "color": "var(--black)"}  #, "bg-color": "var(--main)"}

    about = {"name": "about", "type": "split",
             "left": {"type": "list", "list":
                      [
                          {"title": "Value Added Development", "copy": "Turn a troublesome workflow into time spent else where."},
                          {"title": "Custom Websites", "copy": "We develop the site and teach you to manage it."},
                          {"title": "Integration", "copy": "Connecting services for more efficient workflows."},
                          {"title": "Sharepoint Development", "copy": "Using Office 365? We can help build a site to your needs."}
                      ]},
             "right": {
                 "type": "image",
                 "file": "code.png",
                 "alt": "this is just a placeholder",
                 "title": "Image Placeholder"}
             }

    services = {"name": "services", "type": "split",
                "right": {
                    "type": "image",
                    "file": "code.png",
                    "alt": "this is just a placeholder",
                    "title": "Image Placeholder"},
                "left": {"type": "splash", "headline": "We are excited forward to hearing from you!", "copy": ""}
                }

    test = {"type": "splash", "headline": "Words 'n Shit", "name": 'words', "copy": "I'm like a poet"}
    test_two = {"type": "splash", "headline": "Dynamic Stuff", "name": 'code', "copy": "oh yeah menu"}

    contact_page = {"phone": phone, "twitter": twitter, "owners": owners, "name": "contact", "type": "contact"}

    temp_sections = [home, about, contact_page]
    # temp_sections = [home, services, about, contact_page]
    # temp_sections = [home, services, about, test, test_two, contact_page]

    default = [{"headline": "Hello, World!",
                "copy": "ready to ",
                "name": "home",
                "link": {"url": "admin", "text": "setup"},
                "type": "splash",
                "color": "var(--black)",
                "link-color": "pink"}]

    if db.exists():
        db_sections = db.get_sections()

        print(db_sections)

        if db_sections:

            sections = db_to_objects(db_sections)

            for s in sections:
                print(s.name)

            return render_template("main/index.html", sections=sections)
        else:
            return render_template("main/index.html", sections=default)
    else:
        return render_template("main/index.html", sections=default)


@app.route('/contact', methods=['POST'])
def contact():

    form = request.form
    mailer.send_contact(form["email"], form["subject"], form["message"])
    mailer.send_confirmation(form["email"], form["subject"], form["message"])

    return redirect(url_for('main'))


@app.route('/admin/')
def admin():

    if db.exists():

        print("db exists")

        modal = {"id": "forgot-password", "title": "Forgot Password"}

        if 'auth' in session.keys():
            if session['auth']:
                users = ["one", "two", "three"]

                sections = db_to_objects(db.get_sections())

                return render_template("admin/index.html", user=session['user'], users=users, sections=sections)
        return render_template("admin/portal.html", modal=modal)

    else:

        return render_template("admin/setup.html")


@app.route('/admin/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        # processes form to credentials
        user = request.form['user']
        password = request.form['password']

        user = Users(db=db, uname=user, pword=password)
        ses = Session(user)

        if ses.authenticated:
            serialize_session(ses)
            print(session)
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('admin'))

    else:
        return redirect(url_for('admin'))


@app.route('/admin/logout', methods=['POST', 'GET'])
def logout():

    session.clear()

    return redirect(url_for('admin'))


@app.route('/admin/reset', methods=['POST', 'GET'])
def reset():

    print(request.form)

    return redirect(url_for('admin'))


@app.route('/admin/sections', methods=['POST', 'GET'])
def sections():

    if request.method == 'POST':
        sec = request.form

        if 'action' in sec.keys():
            if sec['action'] == 'delete':

                sec = section_factory(db=db, id=sec['id'])

                print('sec in action')
                print(sec)

                sec.delete()

                return redirect(url_for('admin'))

        if 'section_id' in sec.keys():
            print('edit section')

            print(request.form)
            return redirect(url_for('admin'))
        else:
            print('new section')
            r = request.form
            args = {}

            for i in r:
                if i == 'type':
                    args[i] = int(r[i])
                else:
                    args[i] = r[i]

            sec = section_factory(sec_type=args['type'], db=db, args=args)
            sec.save()

            return redirect(url_for('admin'))


@app.route('/admin/sections/lists/items', methods=['POST', 'GET'])
def list_item():
    print(request.form)
    r = request.form

    print(r['parent'])

    parent = section_factory(db=db, id=r['parent'])
    args = {"parent": r['parent'], "headline": r['headline'], "copy": r['copy']}

    print(r['type'])

    item = section_factory(sec_type=int(r['type']), db=db, args=args)

    print(item)

    parent.add_item(item)

    print("parent.items")
    print(parent.items[0].copy)

    parent.save()

    return redirect(url_for('admin'))


@app.route('/admin/setup', methods=['POST', 'GET'])
def setup():

    if request.method == 'POST':
        if db.exists():
            return redirect(url_for('admin'))
        else:

            r = request.form

            db.init_db()
            db.insert_user(email=r['email'], username=r['user'], password=r['password'], admin=1)
            user = Users(db=db, uname=r['user'], pword=r['password'])
            ses = Session(user)
            serialize_session(ses)

            return redirect(url_for('admin'))

    return redirect(url_for('main'))


@app.route('/test_confirm_email')
def test_confirm():

    email = {"title": "Test Confirm", "message": "This is a test email"}
    return render_template("email/confirmation_email.html", email=email)


def serialize_session(session_obj: Session):
    print("in serialize_session")
    ser = session_obj.serialize()

    for item in ser:
        session[item] = ser[item]

    session['auth'] = True


def db_to_objects(db_sections: tuple) -> [Section]:
    sections = []
    for r in db_sections:

        args = {}
        for i in r:
            if i == 'type':
                args[i] = int(r[i])
            else:
                args[i] = r[i]

        sections.append(section_factory(sec_type=args['type'], db=db, args=args))

    return sections

from flask import render_template, redirect, request, url_for, session, flash, send_from_directory, get_flashed_messages
from config import Config
from kerberusIO.utils.db.users import Users
from kerberusIO.application import app
from kerberusIO.utils.mailer import mailer
from kerberusIO.utils.db.connection import SQLiteDB
from kerberusIO.utils.sessions.session import Session
from kerberusIO.models.Sections import *

from kerberusIO.utils.files.uploader import Uploader

from werkzeug.utils import secure_filename
import os


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

        # print("db_sections")
        # print(db_sections)

        if db_sections:

            section_objs = db_to_objects(db_sections)
            sorted_sections = sort_sections(section_objs)

            return render_template("main/index.html", sections=sorted_sections)
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

        # print("db exists")

        modal = {"id": "forgot-password", "title": "Forgot Password"}

        if 'auth' in session.keys():
            if session['auth']:
                users = ["one", "two", "three"]

                section_objs = db_to_objects(db.get_sections())
                sorted_sections, active = sort_sections(section_objs, True)

                return render_template("admin/index.html", user=session['user'], users=users,
                                       sections=sorted_sections, active=active)
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
            # print(session)
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('admin'))

    else:
        return redirect(url_for('admin'))


@app.route('/admin/logout', methods=['POST', 'GET'])
def logout():

    session.clear()

    return redirect(url_for('admin'))


@app.route('/admin/sections', methods=['POST', 'GET'])
def sections():

    if request.method == 'POST':
        sec = request.form

        print("sec")
        print(sec)

        if 'action' in sec.keys():
            if sec['action'] == 'delete':

                sec = section_factory(db=db, id=sec['id'])

                # print('sec in action')
                # print(sec)

                sec.delete()

                return redirect(url_for('admin'))

        if 'id' in sec.keys():
            # print('edit section')

            print("id is there")
            print(request.form)

            sec = section_factory(db=db, id=request.form['id'])
            secs = get_sections()

            print(sec)
            print(secs)

            print(int(sec.order))
            print(request.form['order'])

            if int(sec.order) != int(request.form['order']):

                old_index = int(sec.order)
                new_index = int(request.form['order'])

                # if new_index > 0:
                print("different")
                len_range = range(len(secs))
                len_ = len(len_range)
                print(len_range)

                moved = secs.pop(old_index)

                print("new_index")
                print(new_index)

                if new_index >= len_ - 1:
                    print("append to end")
                    secs.append(moved)
                elif 0 < new_index < len_ - 1:
                    print("insert in list")
                    secs.insert(new_index, moved)

                inactive = [x for x in secs if x.order < 0]

                for s in reversed(len_range):
                    # the Debugger breaks this cause it runs twice. this try except makes it work

                    try:
                        secs.pop(s - 1)
                    except:
                        pass

                len_range = range(len(secs))
                for i in len_range:
                    if i < len(len_range) - 1:
                        secs[i + 1].set_order(i + 1)
                        print(secs[i + 1].name)
                        print(i + 1)

                if new_index < 0:
                    moved.set_order(-1)
                    secs.append(moved)

                for i in inactive:
                    secs.append(i)

                for s in secs:
                    print(s.order)
                    print(s.name)
                    s.save()

            # print(request.form)
            return redirect(url_for('admin'))
        else:
            # print('new section')
            r = request.form

            print(r)

            args = {}

            for i in r:
                if i == 'type':
                    args[i] = int(r[i])
                else:
                    args[i] = r[i]

            sec = section_factory(sec_type=args['type'], db=db, args=args)

            print("sec.order")
            print(sec.order)

            sec.save()

            return redirect(url_for('admin'))


@app.route('/admin/sections/lists/items', methods=['POST', 'GET'])
def list_item():
    # print(request.form)
    r = request.form

    # print(r['parent'])

    parent = section_factory(db=db, id=r['parent'])
    args = {"parent": r['parent'], "headline": r['headline'], "copy": r['copy']}

    # print(r['type'])

    item = section_factory(sec_type=int(r['type']), db=db, args=args)

    # print(item)

    parent.add_item(item)

    # print("parent.items")
    # print(parent.items[0].copy)

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
    # print("in serialize_session")
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


def sort_sections(section_objects: [Section], admin: bool=False):

    section_objects.sort(key=lambda x: x.order, reverse=False)

    temp_list = []

    sec_i = len(section_objects) - 1

    for _ in section_objects:

        if int(section_objects[sec_i].order) is -1:
            temp_list.append(section_objects.pop(sec_i))

        sec_i -= 1

    sorted = []

    for s in section_objects:
        sorted.append(s)

    for s in temp_list:
        sorted.append(s)

    if admin:

        inactive = len(temp_list)
        active = len(section_objects) - inactive + 1

        print(active)

        return sorted, active
    else:
        return sorted


def get_sections():
    section_rs = db.get_sections()
    if section_rs:
        sec_objs = db_to_objects(section_rs)
        sorted_secs = sort_sections(sec_objs)
        return sorted_secs
    else:
        return []


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        file.filename = "testFileName.jpg"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

    print(get_flashed_messages())
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


@app.route('/uploads_test', methods=['GET', 'POST'])
def upload_test():
    if request.method == 'POST':
        u = Uploader(Config)

        filename = u.upload_file(request, renamed="test_upload")

        return redirect(url_for('uploaded_file', filename=filename))

        pass

    print(get_flashed_messages())
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
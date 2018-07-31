from flask import session, redirect, url_for
import abc
from abc import ABC
from kerberusIO.utils.db.connection import DataBase
import kerberusIO.utils.secrets.user as secrets
from kerberusIO.models.Users import User
import kerberusIO.utils.mailer.mailer as mail
from typing import Union
from kerberusIO.utils.db import calls as db
import time
import datetime


class Session (ABC):
    _db: DataBase
    _user: User

    def __init__(self, db: DataBase, user: User):
        self._db = db
        self._user = user

    @abc.abstractmethod
    def logout(self):
        session.clear()


def valid_password(user_name: str, password: str) -> bool:
    """ tests if the given password given matches the hash in the db for the given user """
    login_qry = "SELECT hash FROM users " \
                "WHERE user_name = %s"

    password_rs = db.get_result_set(login_qry, (user_name,))[0]
    if password_rs:
        hashed = db.get_result_set(login_qry, (user_name,))[0][0]
        if secrets.check_password_hash(password, hashed):
            return True
        else:
            return False
    else:
        return False


def update_password(email: str, password: str) -> None:
    """ updates the password hash in the db for a given username """
    hashed = secrets.hash_password(password)
    update_qry = "UPDATE users SET hash = %s WHERE email = %s"
    db.execute_query(update_qry, (hashed, email))


def update_email(new_email: str, old_email: str) -> dict:
    """ updates the password hash in the db for a given username """
    if is_email_unique(new_email):
        update_email_qry = "UPDATE users SET temp_email = %s, email_confirmed = 0, nonce = %s, nonce_timestamp = %s " \
                           "WHERE email = %s"
        nonce = secrets.generate_nonce()
        nonce_time = time.time()
        time_stamp = datetime.datetime.fromtimestamp(nonce_time)
        args = (new_email, nonce, time_stamp, old_email)

        session["confirmed"] = False
        session["temp_email"] = new_email

        # send email verification
        mail.send_confirmation(new_email, nonce)
        # TODO: send warning to old email

        db.execute_query(update_email_qry, args)

        return {'error': False, 'message': 'Email successfully updated!'}
    else:
        message = 'Email: \"{email}\" is already in use!'.format(email=new_email)
        return {'error': False, 'message': message}


def is_email_unique(email: str) -> bool:
    """ tests if the new email exists in the db """
    unique_query = "SELECT COUNT(*) FROM users WHERE email = %s "
    rs = db.get_result_set(unique_query, (email,))
    if not rs[0][0]:
        return True
    else:
        return False


def is_user_unique(user_name: str) -> bool:
    """ tests if the new email exists in the db """
    unique_query = "SELECT COUNT(*) FROM users WHERE user_name = %s "
    rs = db.get_result_set(unique_query, (user_name,))
    if not rs[0][0]:
        return True
    else:
        return False


def user_exists(user_name: str):
    """ tests if the user exists in the db """
    return not is_user_unique(user_name)


def get_user_by_name(user_name: str) -> User:
    """ gets user from db and loads into an object """
    user_qry = "SELECT user_name, email, email_confirmed, temp_email, admin, " \
               "       first_name, last_name, user_id, banned, active " \
               "    FROM users " \
               "    WHERE user_name = %s"
    rs = db.get_result_set(user_qry, (user_name,))
    db_user = User(db_user=rs)
    db_user.add_characters(get_characters(db_user.user_id))
    return db_user


def login(user_name, password):
    """ does the login for the givens user and password and returns a success/fail message """
    message = "Invalid username or password"
    if valid_password(user_name, password):
        if user_exists(user_name):
            db_user = get_user_by_name(user_name)
            start_session(db_user)
            message = "user successfully logged in"
            return {"error": False, "message": message}
        else:
            return {"error": True, "message": message}
    else:
        return {"error": True, "message": message}


def start_session(user_id: Union[int, str], token: str, device: str):
    """  """
    if isinstance(user_id, int):
        user_id = str(user_id)

    args = (user_id, token, device)
    session_qry = "INSERT INTO sessions ( user_id, token, device) VALUES ( %s, %s, %s )"

    db.execute_query(session_qry, args)


def end_session(user_id: Union[int, str], token: str):
    """  """
    if isinstance(user_id, int):
        user_id = str(user_id)

    args = (user_id, token)
    session_qry = "UPDATE sessions SET active = 0 WHERE user_id = %s and token = %s"

    db.execute_query(session_qry, args)


def create(form_user):
    email = form_user["email"]
    user_name = form_user["user_name"]
    if is_email_unique(email):
        if is_user_unique(user_name):

            first = form_user["first"]
            last = form_user["last"]
            user_name = form_user["user_name"]

            hashed = secrets.hash_password(form_user["password"])
            nonce = secrets.generate_nonce()
            nonce_time = time.time()

            create_qry = "INSERT INTO users (" \
                         "    user_name, email, temp_email, first_name, last_name, hash, nonce, nonce_timestamp" \
                         ") VALUES ( %s, %s, %s, %s, %s, %s, %s, %s )"

            time_stamp = datetime.datetime.fromtimestamp(nonce_time)

            db.execute_query(create_qry, (user_name, email, email, first, last, hashed, nonce, time_stamp))

            mail.send_confirmation(email, nonce)

            user = get_user_by_name(user_name)
            start_session(user)
            return {"error": False, "message": "Account created."}
        else:
            return {"error": True, "message": "Username is taken."}
    else:
        return {"error": True, "message": "Email is taken."}


def add_user(args: tuple):
    create_qry = "INSERT INTO users (" \
                 "    user_name, email, temp_email, first_name, last_name, hash, nonce, nonce_timestamp" \
                 ") VALUES ( %s, %s, %s, %s, %s, %s, %s, %s )"
    try:
        db.execute_query(create_qry, args)
        message = 'User \'{}\' Was created successfully'.format(args[0])
        data = get_user_by_name(args[0]).seralized
        return {"error": False, 'message': message, 'data': data}
    except psycopg2.IntegrityError as err:
        message = 'Integrity Error: {}'.format(str(err))
        return {"error": True, 'message': message, 'data': None}
    except Exception as err:
        message = 'Error: {}'.format(str(err))
        return {"error": True, 'message': message, 'data': None}


def get_characters(user_id: Union[int, str]):
    db_characters = []
    char_qry = "SELECT users.first_name, users.last_name, characters.* FROM users " \
               "    JOIN characters ON users.user_id = characters.user_id " \
               "WHERE characters.user_id = %s;"

    rs = db.get_result_set(char_qry, (user_id,))

    if len(rs):
        for row in rs:
            db_characters.append(Character(db_object=row))
        return db_characters
    else:
        return db_characters


def add_character(char_args: tuple) -> int:
    new_char_qry = "INSERT INTO characters ( user_id, character_name, character_background ) " \
                   "    VALUES ( %s, %s, %s ) RETURNING characters_id"
    return db.execute_query(new_char_qry, char_args)


def get_user_by_nonce(nonce):
    """ gets user from db and loads into an object """
    user_qry = "SELECT user_name, email, email_confirmed, temp_email, admin, first_name, last_name, user_id, banned " \
               "FROM users " \
               "WHERE nonce = %s"

    rs = db.get_result_set(user_qry, (nonce,))

    if rs:
        db_user = User(db_user=rs)
        db_user.add_characters(get_characters(db_user.user_id))
        return db_user
    else:
        return None


def validate_email(old_email: str, new_email: str):
    """ updates a user account to have a valid email """
    validate_qry = "UPDATE users " \
                   "SET " \
                   "    email = %s, " \
                   "    email_confirmed = 1, " \
                   "    temp_email = NULL, " \
                   "    nonce = '', " \
                   "    nonce_timestamp = NULL " \
                   "WHERE email = %s"

    args = (new_email, old_email)
    session["confirmed"] = True
    db.execute_query(validate_qry, args)


def delete_char(char_id):
    """ deletes a character by id """
    delete_qry = "DELETE FROM characters WHERE characters_id = %s;"
    db.execute_query(delete_qry, (char_id,))
    return {"error": False, "message": "character successfully deleted"}


def get_character_by_id(char_id):
    user_qry = "SELECT users.first_name, users.last_name, characters.* FROM users " \
               "    JOIN characters ON users.user_id = characters.user_id " \
               "    WHERE characters.characters_id = %s "
    db_user = db.get_result_set(user_qry, (char_id,))[0]
    return Character(db_object=db_user)


def update_character(char):
    update_qry = "UPDATE characters " \
                 "SET " \
                 "    character_name = %s, " \
                 "    character_background = %s, " \
                 "    character_class = %s, " \
                 "    character_rank = %s, " \
                 "    rank_up = %s, " \
                 "    lance_corporal_ability = %s, " \
                 "    corporal_ability = %s, " \
                 "    sergeant_ability = %s, " \
                 "    staff_sergeant_ability = %s, " \
                 "    tech_sergeant_ability = %s, " \
                 "    gunnery_sergeant_ability = %s, " \
                 "    master_sergeant_ability = %s " \
                 "WHERE characters_id = %s "

    name = str(char.character_name)
    back = str(char.background.type[:3]).lower()
    rank = str(char.rank_value)

    if isinstance(char.character_class, str):
        class_str = str(char.character_class[:3]).upper()
    else:
        class_str = str(char.character_class.type[:3]).upper()

    ranks = str(char.ranks_available)
    char_id = str(char.id)

    lance_corporal = char.abilities["LanceCorporal"]
    corporal = char.abilities["Corporal"]
    sergeant = char.abilities["Sergeant"]
    staff_sergeant = char.abilities["StaffSergeant"]
    tech_sergeant = char.abilities["TechSergeant"]
    gunnery_sergeant = char.abilities["GunnerySergeant"]
    master_sergeant = char.abilities["MasterSergeant"]

    args = (name, back, class_str, rank, ranks, lance_corporal,
            corporal, sergeant, staff_sergeant, tech_sergeant,
            gunnery_sergeant, master_sergeant, char_id)

    db.execute_query(update_qry, args)


def get_users():
    db_players = []
    player_query = "select * from users"
    players = db.get_result_set(player_query)
    if len(players) > 0:
        if isinstance(players[0], tuple):
            for row in players:
                user = get_user_by_name(row[1])
                db_players.append(user)
            return db_players
        else:
            user = get_user_by_name(players[1])
            db_players.append(user)
            return db_players
    else:
        return db_players


def get_user_by_id(user_id) -> User:
    """ gets user from db and loads into an object """
    user_qry = "SELECT user_name, email, email_confirmed, temp_email, admin, " \
               "       first_name, last_name, user_id, banned, active " \
               "    FROM users " \
               "    WHERE user_id = %s"

    rs = db.get_result_set(user_qry, (user_id,))
    if rs:
        db_user = User(db_user=rs)
        db_user.add_characters(get_characters(db_user.user_id))
    else:
        db_user = None

    return db_user


def update_user(db_user: User):
    update_qry = "UPDATE users SET email_confirmed = %s, admin = %s, banned = %s WHERE user_id = %s"
    args = (db_user.confirmed, db_user.admin, db_user.banned, db_user.id)
    db.execute_query(update_qry, args)


def username_exists(username: str) -> bool:
    """ determines if a username exists in the database """
    return not is_user_unique(username)


def token_exists(token: str) -> bool:
    """ tests if the session token exists in the db """
    unique_query = "SELECT COUNT(*) FROM sessions WHERE token = %s"
    rs = db.get_result_set(unique_query, (token,))
    if rs[0][0]:
        return True
    else:
        return False


def deactivate_user_by_id(user_id: Union[int, str]):
    """ deactivates a user by given id """
    if isinstance(user_id, int):
        user_id = str(user_id)

    u = get_user_by_id(user_id)

    deactivate_qry = "UPDATE users SET active = 0 WHERE user_id = %s "

    try:
        db.execute_query(deactivate_qry, (user_id,))
    except Exception as err:
        print(type(err))


if __name__ == '__main__':
    usr = get_user_by_name('asouer')
    pass

import sqlite3
import abc
from abc import ABC
from config import Config
from typing import Union
from kerberusIO.utils.db.schema import schema
from kerberusIO.application import app
from kerberusIO.utils.secrets.hashes import Secrets
# from kerberusIO.models.Sections import section_factory
from flask import g
import os


class DataBase (ABC):

    _config: Config

    def __init__(self, config: Config):
        self._config = config

    @abc.abstractmethod
    def _get_db(self):
        pass

    @abc.abstractmethod
    def execute_query(self, qry: str, args: Union[tuple, str]=None):
        pass

    @abc.abstractmethod
    def get_result_set(self, qry: str, args: tuple) -> [tuple]:
        pass


class SQLiteDB(DataBase):

    _config: Config

    def _get_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(self._config.DATABASE)
        return db

    def execute_query(self, qry: str, args: Union[tuple, str]=None) -> Union[int, None]:
        # TODO: think about returning
        conn = self._get_db()
        cur = conn.cursor()

        if args:
            if isinstance(args, str):
                tup_args = args,
            else:
                tup_args = args
            try:
                cur.execute(qry, tup_args)
                conn.commit()
                return cur.lastrowid

            except sqlite3.Error as err:
                conn.rollback()
                # conn.close()
                print(err)
                raise err
        else:
            try:
                cur.execute(qry)
                conn.commit()
                return cur.lastrowid

            except sqlite3.Error as err:
                conn.rollback()
                # conn.close()
                print(err)
                raise err

    def get_result_set(self, qry: str, args: tuple=None) -> [tuple]:
        conn = self._get_db()
        cur = conn.cursor()
        if args:
            if isinstance(args, str):
                tup_args = args,
            else:
                tup_args = args
            try:
                cur.execute(qry, tup_args)
                rs = cur.fetchall()
                conn.commit()
                return rs
            except sqlite3.Error as err:
                conn.rollback()
                print(err)
        else:
            try:
                cur.execute(qry)
                rs = cur.fetchall()
                conn.commit()
                return rs
            except sqlite3.Error as err:
                conn.rollback()
                print(err)
        print("conn.close()")
        conn.close()

    def exists(self):
        return os.path.isfile(self._config.DATABASE)

    # TODO: The following methods may need to be refactored into their own class

    def init_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            if not os.path.isfile(self._config.DATABASE):
                db = g._database = sqlite3.connect(self._config.DATABASE)
                for qry in schema:
                    print(qry)
                    db.execute(qry)

    def renew_db(self):
        db = getattr(g, '_database', None)
        if db is None:
            if os.path.isfile(self._config.DATABASE):
                db = g._database = sqlite3.connect(self._config.DATABASE)
                for qry in schema:
                    print(qry)
                    db.execute(qry)

    # TODO: The following methods DO need to be refactored into their own class

    def insert_user(self, email: str, username: str, password: str, admin: int = 0) -> int:
        hashed = Secrets.hash_password(password)
        nonce = Secrets.generate_nonce()
        args = (email, email, username, admin, hashed, nonce)
        usr_qry = """
        insert into users
          (email, temp_email, user_name, admin, hash, nonce)
          VALUES ( ?, ?, ?, ?, ?, ?)
        """

        new_user_id = self.execute_query(usr_qry, args)
        self.insert_profile(new_user_id, email)
        return new_user_id

    def insert_profile(self, user_id: int, email: str):
        args = (email, user_id)
        usr_qry = """
        insert into profiles
          (email, user_id)
          VALUES ( ?, ? )
        """

        self.execute_query(usr_qry, args)

    def insert_section(self, name, sec_type, headline, copy):
        args = (name, sec_type, headline, copy)
        sec_qry = """
        INSERT INTO sections
          (name, type, headline, copy)
          VALUES ( ?, ?, ?, ?)
        """

        self.execute_query(sec_qry, args)

    def get_sections(self):
        sec_qry = """
        SELECT * FROM sections
          WHERE type <= 8 AND parent IS NULL
        """

        rs = self.get_result_set(sec_qry)

        sections = []

        print("rs: ")
        print(rs)

        if rs and len(rs):
            for s in rs:

                sections.append({"name": s[2], "type": s[3], "headline": s[4], "copy": s[5],
                                 "id": s[0], "order": s[1], "parent": s[6]})

        return sections


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    with app.app_context():

        db = SQLiteDB(Config)
        db.renew_db()

        email = 'aaron@kerberus.io'
        username = 'asouer'
        fname = 'Aaron'
        lname = 'Souer'

        db.insert_user(email, username, '12345', fname, lname, 1)

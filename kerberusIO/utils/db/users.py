from config import Config
from typing import Union
from kerberusIO.models.Users import User
from kerberusIO.utils.db.connection import DataBase, SQLiteDB

from kerberusIO.application import app


class Users(object):
    _db: DataBase
    _user: User

    def __init__(self, db: DataBase, uname: str, pword: str):
        self._db = db
        self._user = self._get_user(uname, pword)

    def _get_user(self, uname, pword) -> Union[User, None]:
        user_qry = """
        SELECT * FROM users WHERE user_name = ?
        """
        user_rs = self._db.get_result_set(user_qry, uname)
        if user_rs and len(user_rs):
            u = User(password=pword, u_db=user_rs[0])
            return User(password=pword, u_db=user_rs[0])
        else:
            return None

    @property
    def user(self):
        return self._user

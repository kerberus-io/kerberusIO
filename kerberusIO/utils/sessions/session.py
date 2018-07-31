from flask import session
from kerberusIO.models.Users import User
from kerberusIO.utils.db.users import Users
# from kerberusIO.utils.


class Session(object):
    _user: User
    _token: str

    def __init__(self, users: Users):
        self._user = users.user
        self._token = "need to implement"

    @property
    def user(self):
        return self._user

    @property
    def admin(self):
        return self.user.admin

    @property
    def authenticated(self):
        if self.user:
            return self.user.authenticated
        else:
            return False

    def serialize(self):

        serial = {'user': self._user.serialize()}

        if self.admin:
            serial['admin'] = self.admin

        for item in self.__dict__:

            if isinstance(self.__dict__[item], str):
                key = item[1:]
                value = self.__dict__[item]
                serial[key] = value

        return serial

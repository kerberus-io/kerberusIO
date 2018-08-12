import datetime
from kerberusIO.utils.secrets.hashes import Secrets
from kerberusIO.models.Profile import Profile


class User(object):
    _id: int
    _created: datetime.datetime
    _email: str
    _verified: int
    _temp_email: str
    _username: str
    _admin: bool
    _first_name: str
    _last_name: str
    _hash: str
    _nonce: str
    _stamp: datetime.datetime
    _authenticated: bool

    _profile: Profile

    def __init__(self, password: str, u_db=None, p_db=None):
        print(u_db)
        if u_db:
            if Secrets.check_hash(password, u_db[7]):
                self._id = int(u_db[0])

                # TODO: _created needs fixed to actually parse DT
                self._created = u_db[1]

                self._email = u_db[2]
                self._verified = bool(u_db[3])
                self._temp_email = u_db[4]
                self._username = u_db[5]
                self._admin = bool(u_db[6])
                self._nonce = u_db[8]

                # TODO: _stamp needs fixed to actually parse DT
                self._stamp = u_db[9]

                self._authenticated = True

                if u_db:
                    self._profile = Profile(db=u_db)
            else:
                self._authenticated = False
        else:
            pass

    @property
    def id(self):
        if self._authenticated:
            return self._id
        else:
            return None

    @property
    def created(self):
        if self._authenticated:
            return self._created
        else:
            return None

    @property
    def verified(self):
        if self._authenticated:
            return self._verified
        else:
            return False

    @property
    def temp_email(self):
        if self._authenticated:
            return self._temp_email
        else:
            return None

    @property
    def username(self):
        if self._authenticated:
            return self._username
        else:
            return None

    @property
    def admin(self):
        if self._authenticated:
            return self._admin
        else:
            return False

    @property
    def first_name(self):
        if self._authenticated:
            return self._first_name
        else:
            return None

    @property
    def last_name(self):
        if self._authenticated:
            return self._last_name
        else:
            return None

    @property
    def nonce(self):
        if self._authenticated:
            return self._nonce
        else:
            return None

    @property
    def stamp(self):
        if self._authenticated:
            return self._stamp
        else:
            return None

    @property
    def authenticated(self):
        return self._authenticated

    def serialize(self):
        serial = {}

        if self._profile:
            serial['profile'] = self._profile.serialize()

        for item in self.__dict__:
            if isinstance(self.__dict__[item], str):
                key = item[1:]
                value = self.__dict__[item]
                serial[key] = value

        return serial

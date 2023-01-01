import calendar
import datetime
import jwt

from service.user import UserService
from constants import JWT_SECRET, JWT_ALGORITHM

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def gen_token(self, username, password, is_refresh = False):
        user = self.user_service.get_by_username(username)

        if user is None:
            raise Exception()

        if is_refresh != False:
            if not self.user_service.compare_password(user.password, password):
                raise Exception()

        data = {
            'username': user.username,
            'role': user.role
        }

        min10 = datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        data['exp'] = calendar.timegm(min10.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        day100 = datetime.datetime.utcnow() + datetime.timedelta(days=100)
        data['exp'] = calendar.timegm(day100.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        return {'access_token': access_token, 'refresh_token': refresh_token}


    def appruve_revresh(self, refresh_token):
        data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])

        username = data.get('username')
        user = self.user_service.get_by_username(username)

        if user is None:
            raise Exception()

        return self.gen_token(username, user.password, is_refresh=True)

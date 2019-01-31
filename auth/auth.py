import datetime
import jwt
from flask import jsonify

import config
from common import common
from db import db
from models import User, Time


class Auth:
    @staticmethod
    def encode_token(user_id, login_time):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_token(auth_token):
        try:
            payload = jwt.decode(auth_token, config.SECRET_KEY, algorithm='HS256')
            if 'data' in payload and 'id' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    def authenticate(self, username, password):

        userInfo = User.query.filter_by(U_LoginName=username).first()
        if userInfo is None:
            return jsonify(common.falseReturn('', '找不到用户'))
        else:
            if userInfo.verify_password(password):
                login_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                save = Time(U_id=userInfo.U_id, LoginTime=login_time)
                db.session.add(save)
                db.session.commit()
                token = self.encode_token(userInfo.U_id, login_time)
                return jsonify(common.trueReturn(token.decode(), '登录成功'))
            else:
                return jsonify(common.falseReturn('', '密码不正确'))

from functools import wraps

from __init__ import app
from models import User, Nation
from flask import request, jsonify
from db import db
from auth.auth import Auth


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token missing'}), 401
        try:
            x = Auth.decode_token(token)
            current_user = User.query.filter_by(U_id=x['data']['id']).first
        except:
            print(x)
            return jsonify({'message': x}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/')
def hello_world():
    user = User.query.all()
    print(user)
    return 'Hello flask'


@app.route('/hello')
def api_hello():
    user = User.query.all()
    print(user.City)


@app.route('/api/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    if User.query.filter_by(U_LoginName=username).first():
        return 'User existed'
    else:
        save = User(U_LoginName=username)
        save.hash_password(password)
        db.session.add(save)
        db.session.commit()
        return 'success'


@app.route('/api/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(U_LoginName=username).first()
    if not user or not user.verify_password(password):
        return 'Login Failed'
    # print(obj.verify_password(password))
    else:
        return Auth.authenticate(Auth, username, password)


@app.route('/api/getUser', methods=['GET'])
@token_required
def get(current_user):
    users = User.query.all()
    data = []
    for user in users:
        nation = Nation.query.filter_by(N_id=user.U_NationId).first()
        print(user.Nation.N_Name)
        output = {}
        output['UserName'] = user.U_LoginName
        output['Nation'] = nation.N_Name
        data.append(output)
    return jsonify({'data': data})
    # if not user:
    #     jsonify({'message':'No user found'})
    # output = {}
    # output


if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run()

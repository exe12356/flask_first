from __init__ import app
from models import User
from flask import request
from db import db


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
    save = User(U_LoginName=username)
    save.hash_password(password)
    db.session.add(save)
    db.session.commit()
    return 'success'


@app.route('/api/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    obj = User.query.filter_by(U_LoginName=username).first()
    print(obj)
    return 'hello'


if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run()

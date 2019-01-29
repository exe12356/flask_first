from flask import Flask
from db import db

import config

app = Flask(__name__)
app.config.from_object(config)

with app.app_context():
    db.init_app(app)
    db.create_all()

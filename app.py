#!/usr/bin/env python
# encoding=utf-8
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        'db': 'web_app',
        'host': "127.0.0.1"
    }
    app.config['SECRET_KEY'] = 'sadasdsadplosadaskldalskd'
    Bootstrap(app)

    return app


app = create_app()
db = MongoEngine(app)

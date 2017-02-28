#!/usr/bin/env python
# encoding=utf-8

from flask import Flask, request
from flask_mongoengine import MongoEngine
from flask_mongoengine.wtf import model_form
import datetime
import json


def create_app():
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        'db': 'web_app',
        'host': "127.0.0.1"
    }
    app.config['SECRET_KEY'] = 'sadasdsadplosadaskldalskd'
    return app


app = create_app()

db = MongoEngine(app)


class Post_page(db.Document):
    title = db.StringField(max_length=150, required=True)
    publish = db.DateTimeField(default=datetime.datetime.now)
    meta = {
        'collection': 'page',
        'ordering': ['-publish'],
        'strict': False,
        'indexes': [
            {'fields': ['title'], 'unique': True},
            "-publish"
        ]
    }

    tags = db.ListField(db.StringField(max_length=30))
    content = db.StringField()
    classify = db.ListField(db.StringField(max_length=50))


def post_list(data):
    if data:
        return json.loads(data)
    return []


# PostForm = model_form(Post)


@app.route('/post', methods=['GET', 'POST'])
def post_page():
    if request.method == 'POST':
        post_data = request.form
        print post_data.get('classify')
        # page = PostForm(post_data)
        page = Post_page(title=post_data['title'], tags=post_list(post_data.get('tags', '')),
                         classify=post_list(post_data.get('classify', '')), publish=post_data.get('publish', datetime.datetime.now),
                         content=post_data.get('content', ''))

        page.save()
        return 'post ok!'

    return


app.run('0.0.0.0', debug=True)

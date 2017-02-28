#!/usr/bin/env python
# encoding=utf-8
from flask import request
from app import app
from model import Post_page,add_class_tags,get_tags_class
import datetime
import json


def post_list(data):
    if data:
        return json.loads(data)
    return []


@app.route('/post', methods=['GET', 'POST'])
def post_page():
    if request.method == 'POST':
        post_data = request.form
        print post_data.get('classify')
        class_list = post_list(post_data.get('classify', ''))
        tags_list = post_list(post_data.get('tags', ''))
        Post_page.objects(title=post_data['title']).update_one(tags=tags_list,
                         classify=class_list,
                         publish=post_data.get('publish', datetime.datetime.now),
                         content=post_data.get('content', ''), upsert=True)
        # page.save()
        add_class_tags(class_list, tags_list)
        return 'post ok!'
    return 'OK'


@app.route('/')
@app.route('/index/<pageid>')
def index(pageid):
    posts = Post_page.objects.paginate(page=pageid, per_page=10)
    return posts

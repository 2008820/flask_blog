#!/usr/bin/env python
# encoding=utf-8
from flask import request
from app import app
from model import Post_page, add_class_tags, get_tags_class
import datetime
import json


def post_list(data):
    if data:
        return json.loads(data)
    return []


class class_tag(object):
    class_list = []
    tag_list = []


ct = class_tag()
ct.class_list, ct.tag_list = get_tags_class()


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
        ct.class_list, ct.tag_list = get_tags_class()
        return 'post ok!'
    return 'OK'


@app.route('/')
@app.route('/index/<pageid>')
def index(pageid):
    posts = Post_page.objects.paginate(page=pageid, per_page=10)
    return posts


@app.route('/class/<classify>')
def class_view(classify):
    pass


@app.route('/tags/<tag>')
def tag_view(tag):
    pass

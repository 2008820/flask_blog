#!/usr/bin/env python
# encoding=utf-8
from flask import request
from app import app
from model import Post_page
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
        page = Post_page(title=post_data['title'], tags=post_list(post_data.get('tags', '')),
                         classify=post_list(post_data.get('classify', '')),
                         publish=post_data.get('publish', datetime.datetime.now),
                         content=post_data.get('content', ''))

        page.save()
        return 'post ok!'

    return 'OK'

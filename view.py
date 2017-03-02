#!/usr/bin/env python
# encoding=utf-8
from flask import request, render_template
from app import app
from model import Post_page, add_class_tags, get_tags_class,split_page_func
import datetime
import json
import uuid


def post_list(data):
    if data:
        return json.loads(data)
    return []

class setting():
    page = 3
    class_url = {u'关于':'about'}

class class_tag(object):
    class_list = []
    tag_list = []
    page_all = 0

def class_list_obj(cla_list,class_dict):
    claobj = {}
    for classify in cla_list:
        claobj[classify] =class_dict.get(classify, classify)
    return claobj

ct = class_tag()
ct.class_list, ct.tag_list = get_tags_class(setting.class_url)
ct.page_all = len(Post_page.objects) / setting.page + 1


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
                                                               content=post_data.get('content', ''),
                                                               url=uuid.uuid4().__str__(), upsert=True)
        # page.save()
        add_class_tags(class_list, tags_list)
        ct.class_list, ct.tag_list = get_tags_class(setting.class_url)
        ct.page_all = len(Post_page.objects) / setting.page + 1
        return 'post ok!'
    return 'OK'




@app.route('/')
@app.route('/page/<pagenum>')
def index(pagenum=1):
    pagenum_int = int(pagenum)
    posts = Post_page.objects.paginate(page=pagenum_int, per_page=setting.page)
    split_page = split_page_func(ct.page_all, pagenum)
    return render_template("index.html", page=posts, pagenum=split_page, page_class=2, classify=ct.class_list, tags=ct.tag_list)


@app.route('/class/<classify>')
@app.route('/class/<classify>/<pagenum>')
def class_view(classify, pagenum=1):
    pagenum_int = int(pagenum)
    posts = Post_page.objects(classify=classify).paginate(page=pagenum_int, per_page=setting.page)
    split_page = split_page_func(len(Post_page.objects(classify=classify)), pagenum)

    return render_template("index.html", page=posts, kinds=classify, pagenum=split_page, page_class=3, classify=ct.class_list, tags=ct.tag_list)


@app.route('/tags/<tag>')
def tag_view(tag):
    pass

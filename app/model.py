#! /usr/bin/env python
# -*- coding:utf-8 -*-

from flask_login import UserMixin

from creat_app import db


class Post_page(db.Document):
    title = db.StringField(max_length=150, required=True)
    publish = db.DateTimeField()
    meta = {
        'collection': 'page',
        'ordering': ['-publish'],
        'strict': False,
        'indexes': [
            {
                'fields': ['title'],
                'unique': True
            },
            "-publish",
            "url",
        ]
    }
    image_url = db.StringField()
    image_alt = db.StringField()
    url = db.StringField()
    tags = db.ListField(db.StringField(max_length=30))
    content = db.StringField()
    classify = db.ListField(db.StringField(max_length=50))


class Class_tags(db.Document):
    meta = {'collection': 'index'}
    _id = db.StringField(required=True)
    classifyList = db.ListField(db.StringField(max_length=50))
    tagList = db.ListField(db.StringField(max_length=30))


class User(UserMixin):
    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    pass


# 聚合标签和分类
def add_class_tags(class_list={}, tags_list=[]):
    if class_list:
        for classify in class_list:
            print classify
            if not Class_tags.objects(_id='index').filter(
                    classifyList=classify):
                Class_tags.objects(_id='index').update_one(
                    push__classifyList=classify, upsert=True)
    if tags_list:
        for tag in tags_list:
            if not Class_tags.objects(_id='index').filter(tagList=tag):
                Class_tags.objects(_id='index').update_one(
                    push__tagList=tag, upsert=True)


# class list 2 dict
def class_list_obj(cla_list, class_dict):
    claobj = {}
    for classify in cla_list:
        claobj[classify] = class_dict.get(classify, classify)
    return claobj


def get_tags_class():
    try:
        class_tag = Class_tags.objects.get(_id='index')
        class_list = class_tag.classifyList
        tag_list = class_tag.tagList
        return class_list, tag_list
    except:
        return [], []


def get_index_data(page):
    posts = Post_page.objects.paginate(page=page, per_page=10)
    return posts


# 分页
def split_page_func(page_all, pagenum):
    if pagenum > 6 and pagenum <= page_all - 5:
        split_page = range(pagenum - 5, pagenum + 5)
    elif pagenum > 6 and page_all < 12:
        split_page = range(pagenum - 5, page_all + 1)
    elif pagenum > (page_all - 5) and page_all > 10:
        split_page = range(page_all - 9, page_all + 1)
    elif pagenum <= 6 and page_all > 10:
        split_page = range(1, 10)
    elif pagenum <= 6 and page_all <= 10:
        split_page = range(1, page_all + 1)
    else:
        split_page = range(10)
    return split_page


if __name__ == '__main__':
    get_index_data()

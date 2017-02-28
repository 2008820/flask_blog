#! /usr/bin/env python
# -*- coding:utf-8 -*-

from app import db
import datetime


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


class Class_tags(db.Document):
    meta = {
        'collection': 'index'
    }
    _id = db.StringField(required=True)
    classifyList = db.ListField(db.StringField(max_length=50))
    tagList = db.ListField(db.StringField(max_length=30))


# 聚合标签和分类
def add_class_tags(class_list=[], tags_list=[]):
    if class_list:
        for classify in class_list:
            print classify
            if not Class_tags.objects(_id='index').filter(classifyList=classify):
                Class_tags.objects(_id='index').update_one(push__classifyList=classify, upsert=True)
    if tags_list:
        for tag in tags_list:
            if not Class_tags.objects(_id='index').filter(tagList=tag):
                Class_tags.objects(_id='index').update_one(push__tagList=tag, upsert=True)


def get_tags_class():
    class_tag = Class_tags.objects.get(_id='index')
    class_list = class_tag.classifyList
    tag_list = class_tag.tagList
    return class_list,tag_list

def get_index_data(page):
    posts = Post_page.objects.paginate(page=page, per_page=10)
    return posts



if __name__ == '__main__':
    get_index_data()

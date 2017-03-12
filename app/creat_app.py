#!/usr/bin/env python
# encoding=utf-8
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
import sys
from web_conf import user, passwd
import os
import re
reload(sys)
sys.setdefaultencoding('utf-8')
root_path = os.path.abspath('./')
image_path = root_path + '/image'

def timestamp(time, type=False):
    if type:
        return time.strftime("%Y年%m月%d日 %H时%M分%S秒")
    return time.strftime("%Y年%m月%d日")

if not os.path.exists("image"):
    os.mkdir("image")

def clean_html_tag(content):
    html = re.sub('<[\s\S]*?>', "", content)
    html = re.sub('<[\s\S]+>*', "", html)
    return html

def set_url(name, kinds=0):
    if kinds == 0:
        return "/detail/" + str(name)
    if kinds == 1:
        return "/tags/" + str(name)
    if kinds == 2:
        return "/page/" + str(name)
    if kinds == 3:
        return "/class/" + str(name)
login_manager = LoginManager()
def create_app():
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        'db': 'web_app',
        'host': "127.0.0.1"
    }
    app.config["posts_num"] = 6
    app.config['classify_url'] = {}
    app.config['UPLOAD_FOLDER'] = image_path
    app.config['SECRET_KEY'] = 'sadasdsadplosadaskldalskd'
    app.config['author'] = user
    app.config['passwd'] = passwd
    app.config['qiniuhost'] = "http://oml5dvid2.bkt.clouddn.com/"
    app.add_template_filter(timestamp, 'timestamp')
    app.add_template_filter(set_url, 'set_url')
    app.add_template_filter(clean_html_tag, 'clean_tag')
    return app


app = create_app()
db = MongoEngine(app)
login_manager.init_app(app)

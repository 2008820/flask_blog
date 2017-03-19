#!/usr/bin/env python
# encoding=utf-8
import datetime

from flask import request, render_template, Response, url_for, redirect, g
from flask_login import login_user, login_required,logout_user, current_user

from creat_app import app, login_manager, cache
from model import Post_page, add_class_tags, get_tags_class, split_page_func,User
from function import get_backgroud_img
try:
    import qiniu_image
except:
    exit("请安装 pip install qiniu")
import hashlib
import uuid
import os
import re


def post_list(data):
    if data:
        return data.split(',')
    return []



# class_tag 缓存
class class_tag(object):
    class_list = {}
    tag_list = []
    page_all = 0


def class_list_obj(cla_list, class_dict):
    claobj = {}  # key cn vaule en
    for classify in cla_list:
        claobj[classify] = class_dict.get(classify, classify)
    return claobj


ct = class_tag()
class_list, ct.tag_list = get_tags_class()
ct.class_list = class_list_obj(class_list, app.config["classify_url"])

if len(Post_page.objects) % app.config["posts_num"] == 0:
    ct.page_all = len(Post_page.objects) / app.config["posts_num"]
else:
    ct.page_all = len(Post_page.objects) / app.config["posts_num"] + 1

@login_manager.user_loader
def user_loader(user):
    user = User()
    return user


@app.before_request
def get_header():
    data = request.environ
    # print data["werkzeug.request"].get("REMOTE_ADDR", "")
    # print data["werkzeug.request"].__dict__
    cdata = data["werkzeug.request"]
    # print cdata.__dict__
    # print dir(cdata)
    print cdata.method, cdata.host, cdata.referrer, cdata.remote_addr, cdata.path, cdata.routing_exception, data["HTTP_USER_AGENT"]


@app.route('/admin/post', methods=['GET', 'POST'])
@login_required
def post_page():
    if request.method == 'POST':
        post_data = request.form
        class_list = post_list(post_data.get('classify', ''))
        tags_list = post_list(post_data.get('tags', ''))
        content = post_data.get('content', '')
        publish_time = post_data.get('publish')
        if not publish_time.strip():
            publish_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        image_url_list = re.findall('<img[\s\S]*?src="(.+?)"[\s\S]*?.*?a?l?t?=?"?(.*?)"?', content)
        print image_url_list
        if image_url_list:
            image_url = image_url_list[0][0]
            alt = image_url_list[0][1]
            if not alt:
                alt = 'febrain的位置'
        else:
            image_url = ""
            alt = ""
        title = post_data['title']
        md5 = hashlib.md5()
        md5.update(title)
        url = md5.hexdigest()
        Post_page.objects(title=title).update_one(tags=tags_list,
                                                               classify=class_list,
                                                               publish=publish_time,
                                                               content=content,
                                                               image_url=image_url,
                                                               image_alt=alt,
                                                               url=url, upsert=True)
        # page.save()
        add_class_tags(class_list, tags_list)
        class_list, ct.tag_list = get_tags_class()
        ct.class_list = class_list_obj(class_list, app.config["classify_url"])
        ct.page_all = len(Post_page.objects) / app.config["posts_num"] + 1
        return 'post ok!'
    return render_template('admin/post.html')

@app.route("/admin/edit", methods=["GET","POST"])
def edit_article():
    article_id = request.args.get("id")
    if article_id:
        article = Post_page.objects.get(url=article_id)
        if article.classify:
            article.classify = ",".join(article.classify)
        else:
            article.classify = ""
        if article.tags:
            article.tags = ",".join(article.tags)
        else:
            article.tags = ""
        return render_template("admin/editor.html", article=article)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        postData = request.form
        if app.config['author'] == postData.get('user','') and app.config['passwd'] == postData.get('passwd',''):
            user = User()
            user.id = app.config['author']
            login_user(user)
            return redirect(url_for("post_page"))
        return """ Bad login """
    if current_user.is_authenticated:
        return redirect(url_for("post_page"))
    return render_template('admin/login.html')

@app.route("/logout")
def logout():
    logout_user()
    return 'Logged out'

@app.route("/ImageUpdate", methods=["POST"])
def GetImage():
    file = request.files['myFileName']
    if file == None:
        result = r"error|未成功获取文件，上传失败"
        res = Response(result)
        res.headers["ContentType"] = "text/html"
        res.headers["Charset"] = "utf-8"
        return res
    else:
        if file:
            if not app.config.get("qiniuhost",""):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                imgUrl = "/image/"
                res = Response(imgUrl)
                res.headers["ContentType"] = "text/html"
                res.headers["Charset"] = "utf-8"
                return res
            qiniu_image.upload(file)
            return app.config["qiniuhost"] + file.filename

@app.route('/image/<name>')
def get_image(name):
    image = file(app.config['UPLOAD_FOLDER'] + '/' + name)
    resp = Response(image, mimetype="image/jpeg")
    return resp






def view_tag_class(kinds, vaule, numnow, **context):
    pagenum_int = int(numnow)
    if kinds == "tags":
        db_objects = Post_page.objects(tags=vaule)
        page_class = 1
    elif kinds == 'classify':
        db_objects = Post_page.objects(classify=vaule)
        page_class = 3
    posts = db_objects.paginate(page=pagenum_int, per_page=app.config["posts_num"])
    all_page = len(db_objects) / app.config["posts_num"] + 1
    split_page_num = split_page_func(all_page, pagenum_int)
    split_page_url = [vaule + '/' + str(item) for item in split_page_num]
    return render_template("index.html", page=posts, kinds=vaule, pagenum=split_page_num, page_class=page_class,
                           classify=ct.class_list, tags=ct.tag_list, split_page_url=split_page_url,
                           current_page=pagenum_int, **context)


def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return str(path+args)

@app.route('/')
@app.route('/page/<pagenum>')
# @cache.cached(timeout=app.config['cache_time'], key_prefix=make_cache_key)
def index(pagenum=1):
    get_backgroud_img()
    pagenum_int = int(pagenum)
    posts = Post_page.objects.paginate(page=pagenum_int, per_page=app.config["posts_num"])
    split_page = split_page_func(ct.page_all, pagenum_int)
    if current_user.is_authenticated:
        posts.edit = True
    return render_template("index.html", page=posts, pagenum=split_page, page_class=2, classify=ct.class_list,
                           tags=ct.tag_list, current_page=pagenum_int, kinds="")


@app.route('/class/<classify>')
@app.route('/class/<classify>/<pagenum>')
# @cache.cached(timeout=app.config['cache_time'], key_prefix=make_cache_key)
def class_view(classify, pagenum=1):
    return view_tag_class('classify', classify, pagenum)


@app.route('/tags/<tag>')
@app.route('/tags/<tag>/<pagenum>')
# @cache.cached(timeout=app.config['cache_time'], key_prefix=make_cache_key)
def tag_view(tag, pagenum=1):
    return view_tag_class('tags', tag, pagenum)

@app.route('/detail/<pageId>')
# @cache.cached(timeout=app.config['cache_time'], key_prefix=make_cache_key)
def get_page_detail(pageId):
    dataObj = Post_page.objects(url=pageId)
    for item in dataObj:
        title = item.title
    pageObj = dataObj.paginate(page=1, per_page=app.config["posts_num"])
    if current_user.is_authenticated:
        pageObj.edit = True
    return render_template("detail.html", page=pageObj, classify=ct.class_list, tags=ct.tag_list,title=title)
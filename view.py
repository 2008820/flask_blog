#!/usr/bin/env python
# encoding=utf-8
from flask import request, render_template, Response
from app import app
from model import Post_page, add_class_tags, get_tags_class, split_page_func
import datetime
import json
import uuid
import os


def post_list(data):
    if data:
        return data.split(',')
    return []


class setting():
    page = 3
    class_url = {}


class class_tag(object):
    class_list = {}
    tag_list = []
    page_all = 0


def class_list_obj(cla_list, class_dict):
    claobj = {}
    for classify in cla_list:
        claobj[classify] = class_dict.get(classify, classify)
    return claobj


ct = class_tag()
_, ct.tag_list = get_tags_class(setting.class_url)
if len(Post_page.objects) % setting.page == 0:
    ct.page_all = len(Post_page.objects) / setting.page
else:
    ct.page_all = len(Post_page.objects) / setting.page + 1


@app.route('/post', methods=['GET', 'POST'])
def post_page():
    if request.method == 'POST':
        post_data = request.form
        print post_data
        print post_data.get('content', 'nonecontent')
        print post_data.get('classify')
        class_list = post_list(post_data.get('classify', ''))
        tags_list = post_list(post_data.get('tags', ''))
        publish_time = post_data.get('publish', datetime.datetime.now())
        if isinstance(publish_time, str):
            publish_time = datetime.datetime.strptime(publish_time, "%Y-%m-%d %H:%M:%S")
        print publish_time
        Post_page.objects(title=post_data['title']).update_one(tags=tags_list,
                                                               classify=class_list,
                                                               publish=publish_time,
                                                               content=post_data.get('content', ''),
                                                               url=uuid.uuid4().__str__(), upsert=True)
        # page.save()
        add_class_tags(class_list, tags_list)
        ct.class_list, ct.tag_list = get_tags_class(setting.class_url)
        ct.page_all = len(Post_page.objects) / setting.page + 1
        return 'post ok!'
    return render_template('admin/post.html')


@app.route("/ImageUpdate", methods=["POST"])
def GetImage():
    print '111111111'
    print dir(request)
    print request.files
    file = request.files['wangEditorH5File']
    print '2222222222'
    if file == None:
        result = r"error|未成功获取文件，上传失败"
        res = Response(result)
        res.headers["ContentType"] = "text/html"
        res.headers["Charset"] = "utf-8"
        return res
    else:
        # if file and allowed_file(file.filename):
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            imgUrl = "/image/" + filename
            res = Response(imgUrl)
            res.headers["ContentType"] = "text/html"
            res.headers["Charset"] = "utf-8"
            return res

@app.route('/image/<name>')
def get_image(name):
    print name
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
    posts = db_objects.paginate(page=pagenum_int, per_page=setting.page)
    all_page = len(db_objects) / setting.page + 1
    split_page_num = split_page_func(all_page, pagenum_int)
    print all_page, split_page_num
    split_page_url = [vaule + '/' + str(item) for item in split_page_num]
    return render_template("index.html", page=posts, kinds=vaule, pagenum=split_page_num, page_class=page_class,
                           classify=ct.class_list, tags=ct.tag_list, split_page_url=split_page_url,
                           current_page=pagenum_int, **context)




@app.route('/')
@app.route('/page/<pagenum>')
def index(pagenum=1):
    pagenum_int = int(pagenum)
    posts = Post_page.objects.paginate(page=pagenum_int, per_page=setting.page)
    split_page = split_page_func(ct.page_all, pagenum_int)
    return render_template("index.html", page=posts, pagenum=split_page, page_class=2, classify=ct.class_list,
                           tags=ct.tag_list, current_page=pagenum_int)


@app.route('/class/<classify>')
@app.route('/class/<classify>/<pagenum>')
def class_view(classify, pagenum=1):
    return view_tag_class('classify', classify, pagenum)


@app.route('/tags/<tag>')
@app.route('/tags/<tag>/<pagenum>')
def tag_view(tag, pagenum=1):
    return view_tag_class('tags', tag, pagenum)

@app.route('/detail/<pageId>')
def get_page_detail(pageId):
    pageObj = Post_page.objects(url=pageId).paginate(page=1, per_page=setting.page)
    print pageObj.items
    return render_template("detail.html", page=pageObj, classify=ct.class_list,tags=ct.tag_list)
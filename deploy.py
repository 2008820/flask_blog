#!/usr/bin/env python
# encoding=utf-8
from fabric.api import *
from fabric.contrib.files import exists
from app.web_conf import host, host_passwd
APP_PATH = "/root/blog"


# @parallel(pool_size=12)
def put_app():
    if not exists(APP_PATH):
        run("mkdir -p " + APP_PATH)
    with settings(warn_only=True):
        local("tar -zcvf blog_app.tar.gz * ")
    put("blog_app.tar.gz", APP_PATH)
    with cd(APP_PATH):
        run("tar -zxvf blog_app.tar.gz")
        run("rm blog_app.tar.gz")
    local("rm blog_app.tar.gz")


if __name__ == "__main__":
    env.hosts = host
    env.password = host_passwd
    execute(put_app)

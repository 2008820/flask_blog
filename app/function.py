#!/usr/bin/env python
# encoding=utf-8
import requests
import re
import os
import datetime
path = os.path.abspath(".")
temp_time = datetime.datetime.today().day


def get_backgroud_img():
    global temp_time
    now_day = datetime.datetime.today().day
    if temp_time == now_day:
        return
    print("抓取")
    temp_time = now_day
    url = "http://cn.bing.com"
    html = requests.get(url).content
    background_image = re.findall('g_img={url: "(.+?)"', html)
    if background_image:
        image_url = background_image[0]
        if image_url.startswith("//"):
            image_url = "http:" + image_url
        else:
            image_url = url + image_url
        open(path + "/templates/config_html/backgroudUrl.html",
             'w').write(image_url)
    else:
        pass


if __name__ == "__main__":
    get_backgroud_img()

#!/usr/bin/env python
# encoding=utf-8
import re
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')
name = './Ghost 开源博客平台 _ Ghost中文网_files/'

old_html = open('old_index.html').read()
soup = BeautifulSoup(old_html, 'html5lib')


def replace_name(ftag, stag):
    link_list = soup.find_all(ftag)
    for link in link_list:
        hreftag = link.get(stag)
        if hreftag:
            if name in hreftag:
                if not hreftag.endswith('html'):
                    new_href = hreftag.replace(
                        name, "{{url_for('static',filename='") + "')}}"
                    print link
                    link[stag] = new_href
                    print link
                # print link


replace_name('link', 'href')
replace_name('script', 'src')
replace_name('img', 'src')

open('admin/post.html', 'w').write(str(soup))

#!/usr/bin/env python
# encoding=utf-8
import requests

data = {'title': "asdasdas123123", 'content': 'asadsadsdsds', 'classify': '["asdsa", "sdfdsf","asdsasdasd12"]','tags':'["asdsa", "sdfdsf"]'}
headers = {'csrf_token': 'asdsad'}

html = requests.post('http://0.0.0.0:5000/post', data=data, headers=headers).content
open('html.html', 'w').write(html)

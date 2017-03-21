#!/usr/bin/env python
# encoding=utf-8
import requests
import uuid
for i in range(1):
    data = {
        'title': uuid.uuid4().__str__(),
        'content': 'asadsadsdsds',
        'classify': '',
        'tags': ''
    }
    headers = {'csrf_token': 'asdsad'}
    html = requests.post(
        'http://0.0.0.0:5000/post', data=data, headers=headers).content

# open('html.html', 'w').write(html)

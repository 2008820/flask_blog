#!/usr/bin/env python
# encoding=utf-8
import app.view
# import bjoern
from app.creat_app import app
# from werkzeug.contrib.fixers import ProxyFix
# app.wsgi_app = ProxyFix(app.wsgi_app)
app.run('0.0.0.0', debug=True)
# bjoern.listen(app, "0.0.0.0", 5000, reuse_port=True)
# bjoern.run()

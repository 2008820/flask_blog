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

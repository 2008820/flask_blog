from qiniu import Auth, put_data
from web_conf import access_key, secret_key

# access_key = ''
# secret_key = ''
q = Auth(access_key, secret_key)
bucket_name = 'flask-blog'


def upload(file):
    key = file.filename
    token = q.upload_token(bucket_name, key, 3600)
    ret, info = put_data(token, key, file)

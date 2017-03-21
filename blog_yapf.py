import os
path = os.path.abspath('.')
from yapf.yapflib.yapf_api import FormatCode
print path


def sytle_path(dir):
    if os.path.isdir(dir):
        for _file in os.listdir(dir):
            path = dir + '/' + _file
            sytle_path(path)
    else:
        if dir.endswith(".py"):
            print dir
            os.system("yapf -i {}".format(dir))


file_path = path
sytle_path(file_path)

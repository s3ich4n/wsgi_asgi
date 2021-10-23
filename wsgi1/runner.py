#
# WSGI 앱을 구동
#
# @author      Seongeun Yu (s3ich4n@gmail.com)
# @date        2021/10/23 17:07 created.
# @modified    2021/10/23 17:07 modified.
# @copyright   MIT License
#


from wsgiref.simple_server import make_server

from app_base import application

with make_server('', 8000, application) as httpd:
    print("going to serve port 8000...")
    httpd.serve_forever()

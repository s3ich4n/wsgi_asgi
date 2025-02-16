#
# WSGI 앱을 구동
#   wsgiref의 simple_server를 통해 구동함
#
# @author      Seongeun Yu (s3ich4n@gmail.com)
# @date        2021/10/23 17:07 created.
# @modified    2021/10/23 17:07 modified.
# @copyright   MIT License
#


from wsgiref.simple_server import make_server

from wsgi.pep_example.app_base_class import AppClass


with make_server('', 8000, AppClass) as httpd:
    print("going to serve port 8000...")
    httpd.serve_forever()

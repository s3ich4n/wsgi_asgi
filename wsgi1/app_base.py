#
# WSGI 로 서비스되는 웹 애플리케이션
#   출처: https://www.python.org/dev/peps/pep-0333/
#
# @author      Seongeun Yu (s3ich4n@gmail.com)
# @date        2021/10/23 17:07 created.
# @modified    2021/10/23 17:07 modified.
# @copyright   MIT License
#


from wsgiref.util import setup_testing_defaults


def application(
        environ,
        start_response,
):
    """

    :param environ:
    :param start_response:
    :return:
    """
    setup_testing_defaults(environ)

    #
    # body는 아래와 같은 방식으로 준비한다.
    # response_body = [
    #     (
    #         "wanna-say: s3ich4n rules!".encode("UTF-8")
    #     )
    # ]
    #
    response_body = "wanna-say: s3ich4n rules!".encode("UTF-8")

    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body))),
    ]

    # Callback...
    # 'start_response()' callable as specified by PEP 3333
    start_response(status, response_headers)

    return [(response_body), ]

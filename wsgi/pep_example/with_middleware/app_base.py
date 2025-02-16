#
# WSGI 로 서비스되는 웹 애플리케이션
#   출처: https://www.python.org/dev/peps/pep-0333/
#
# @author      Seongeun Yu (s3ich4n@gmail.com)
# @date        2021/10/23 17:07 created.
# @modified    2021/10/23 17:07 modified.
# @copyright   MIT License
#


def easy_application(
        environ,
        start_response,
):
    """

    :param environ:
    :param start_response:
    :return:
    """

    #
    # body는 아래와 같은 방식으로 준비한다.
    # response_body = [
    #     (
    #         "wanna-say: s3ich4n rules!".encode("UTF-8")
    #     )
    # ]
    #

    #
    # 문자열 encode를 미들웨어 단에서 처리하려면
    # 그냥 파이썬 변수를 넘겨줘서, 마지막에 처리하도록 세팅한다.
    response_body = "wanna say paris?"

    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body))),
    ]

    # Callback...
    # 'start_response()' callable as specified by PEP 3333
    start_response(status, response_headers)

    return [response_body, ]

#
# 클래스를 사용한 앱/프레임워크 사이드 구현
#   출처: https://www.python.org/dev/peps/pep-0333/
#
# @author      Seongeun Yu (s3ich4n@gmail.com)
# @date        2021/10/23 20:07 created.
# @modified    2021/10/23 20:07 modified.
# @copyright   MIT License
#


class AppClass:
    """ 클래스를 사용한 구현체를 의미

    AppClass 앱을 호출하는 것은 "해당 객체"를 리턴하는 것을 의미한다.

    이는, 사양에서 요구하는 "앱 Callable"의 iterable 리턴값이다.

    AppClass의 인스턴스를 앱 오브젝트로 대신 쓰려면,
    `__call__` 객체를 구현해야되고
    서버/게이트웨이 에서 쓸 인스턴스를 생성해야한다.

    """

    # 문자열 encode를 미들웨어 단에서 처리하려면
    # 그냥 파이썬 변수를 넘겨줘서, 마지막에 처리하도록 세팅한다.
    RES = "ultimate"
    #
    # 여기가 마지막이면, UTF-8 인코딩을 할 수 있도록 해야한다.
    # RES = "wanna-say: s3ich4n rules!".encode("UTF-8")

    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        status = '200 OK'
        response_headers = [
            ('Content-Type', 'text/plain'),
            ('Content-Length', len(self.RES)),
        ]
        self.start(status, response_headers)

        yield self.RES

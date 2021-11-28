#
# PEP 3333, Middleware 예시
#
# @author      Seongeun Yu (s3ich4n@gmail.com)
# @date        2021/11/28 16:06 created.
# @modified    2021/11/28 16:06 modified.
# @copyright   MIT License
#
from wsgi1.pep_example.app_base_class import AppClass
from wsgi1.pep_example.piglatin import piglatin
from wsgi1.pep_example.server import run_with_cgi
from wsgi1.pep_example.app_base import easy_application


class LatinIter:

    """Transform iterated output to piglatin, if it's okay to do so

    Note that the "okayness" can change until the application yields
    its first non-empty bytestring, so 'transform_ok' has to be a mutable
    truth value.
    """

    def __init__(self, result, transform_ok):
        if hasattr(result, 'close'):
            self.close = result.close
        self._next = iter(result).__next__
        self.transform_ok = transform_ok

    def __iter__(self):
        return self

    def __next__(self):
        data = self._next()
        if self.transform_ok:
            return piglatin(data)   # call must be byte-safe on Py3
        else:
            return data


class Latinator:

    # by default, don't transform output
    transform = False

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):

        transform_ok = []

        def start_latin(status, response_headers, exc_info=None):

            # Reset ok flag, in case this is a repeat call
            del transform_ok[:]

            for name, value in response_headers:
                if name.lower() == 'content-type' and value == 'text/plain':
                    transform_ok.append(True)
                    # Strip content-length if present, else it'll be wrong
                    response_headers = [(name, value)
                        for name, value in response_headers
                            if name.lower() != 'content-length'
                    ]
                    break

            write = start_response(status, response_headers, exc_info)

            if transform_ok:
                def write_latin(data):
                    write(piglatin(data))   # call must be byte-safe on Py3
                return write_latin
            else:
                return write

        return LatinIter(self.application(environ, start_latin), transform_ok)


# Run foo_app under a Latinator's control,
# Using the example CGI gateway
#
#   아래 로직에 대해 주석해제 후 사용.
#
#   1. 클래스 형식의 WSGI 애플리케이션 구현체,
#      Latinator 미들웨어를 통과함.
# run_with_cgi(Latinator(easy_application))
#   2. 메소드 형식의 WSGI 애플리케이션 구현체
#      Latinator 미들웨어를 통과함.
# run_with_cgi(Latinator(AppClass))

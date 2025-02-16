#
# 서버/게이트웨이 사이드 구현
#   출처: https://www.python.org/dev/peps/pep-0333/
#
# @author      Seongeun Yu (s3ich4n@gmail.com)
# @date        2021/10/24 20:21 created.
# @modified    2021/10/24 20:21 modified.
# @copyright   MIT License
#


import sys


# 시스템 인코딩 및 non-decodeable bytes에 연관된 에러 핸들러
enc, esc = sys.getfilesystemencoding(), 'surrogateescape'


def unicode_to_wsgi(u):
    """ 환경변수 값을 WSGI의 'bytes-as-unicode" 문자열로 변경한다.

    iso-8859-1은 Latin-1 인코딩 값을 의미한다.

    :param u:
    :return:
    """
    return u.encode(enc, esc).decode('iso-8859-1')


def wsgi_to_bytes(s):
    """ bytes 값으로 인코딩한다.

    :param s:
    :return:
    """
    return s.encode('iso-8859-1')


def run_with_cgi(application):
    """

    :param application:
    :return:
    """
    # environ = {k: unicode_to_wsgi(v) for k, v in os.environ.items()}
    environ = {'wsgi.input': sys.stdin.buffer, 'wsgi.errors': sys.stderr,
               'wsgi.version': (1, 0), 'wsgi.multithread': False,
               'wsgi.multiprocess': True, 'wsgi.run_once': True}

    if environ.get('HTTPS', 'off') in ('on', '1'):
        environ['wsgi.url_scheme'] = 'https'
    else:
        environ['wsgi.url_scheme'] = 'http'

    headers_set = []
    headers_sent = []

    def write(data):
        out = sys.stdout.buffer

        if not headers_set:
            raise AssertionError("write() before start_response()")

        elif not headers_sent:
            # Before the first output, send the stored headers
            status, response_headers = headers_sent[:] = headers_set
            out.write(wsgi_to_bytes('Status: %s\r\n' % status))
            for header in response_headers:
                out.write(wsgi_to_bytes('%s: %s\r\n' % header))
            out.write(wsgi_to_bytes('\r\n'))

        out.write(data)
        out.flush()

    def start_response(status, response_headers, exc_info=None):
        """ 해당 값으로 start_response 함수를 전달한다.

        :param status:
        :param response_headers:
        :param exc_info:
        :return:
        """
        if exc_info:
            try:
                if headers_sent:
                    # Re-raise original exception if headers sent
                    raise exc_info[1].with_traceback(exc_info[2])
            finally:
                exc_info = None     # avoid dangling circular ref
        elif headers_set:
            raise AssertionError("Headers already set!")

        headers_set[:] = [status, response_headers]

        # Note: error checking on the headers should happen here,
        # *after* the headers are set.  That way, if an error
        # occurs, start_response can only be re-called with
        # exc_info set.

        return write

    # 앱 호출을 "했다" 고 가정하자.
    result = application(environ, start_response)
    try:
        for data in result:
            if data:    # don't send headers until body appears
                write(data)
        if not headers_sent:
            write('')   # send headers now if body was empty
    finally:
        if hasattr(result, 'close'):
            result.close()

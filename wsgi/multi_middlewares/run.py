from wsgiref.simple_server import make_server


class Middleware1:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # 애플리케이션에 "요청이" 처리되기 전에,
        # 이 미들웨어를 통해 하고싶은 작업을 합니다.

        print("before middleware 1 access")
        response = self.app(environ, start_response)

        # 애플리케이션이 처리하고 난 "응답에",
        # 이 미들웨어를 통해 하고싶은 작업을 합니다.

        print("after middleware 1 access")
        return response


class Middleware2:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # 애플리케이션에 "요청이" 처리되기 전에,
        # 이 미들웨어를 통해 하고싶은 작업을 합니다.

        print("before middleware 2 access")

        response = self.app(environ, start_response)

        # 애플리케이션이 처리하고 난 "응답에",
        # 이 미들웨어를 통해 하고싶은 작업을 합니다.

        print("after middleware 2 access")
        return response


class MyApp:
    def __call__(self, environ, start_response):
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        response = b'Hello, World!'
        start_response(status, headers)
        return [response]


# 애플리케이션은 미들웨어 1, 2순으로 돌도록 설정되었습니다.
app = MyApp()
app = Middleware1(app)
app = Middleware2(app)

# 서버는 wsgiref에서 제공하는 makeserver를 사용합시다.
httpd = make_server('', 8800, app)
httpd.serve_forever()

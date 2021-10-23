# 요청이 들어오면?

## soket 단 처리

+ socket 단에서 처리 시작

파일: `python3.8 > socketserver.py`

```python
class BaseRequestHandler:

    """Base class for request handler classes.
    (중략)
    """

    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        try:
            self.handle()       # <- 해당부분부터 처리 시작 
        finally:
            self.finish()       # <- 응답을 처리하는 부분 참고
```

서버 핸들러 (simplehandler, http/1.0의 동기처리용 핸들러) 생성

+ wsgiref 시작. application 로드

+ 우리가 작성한 app 구동, 이후 리턴값 전달.
    + 이 때,
        + `environ` 파라미터는 환경변수 값을 받는다.
        + `start_response` 파라미터에는 BaseHandler.start_response 값을 받는다.

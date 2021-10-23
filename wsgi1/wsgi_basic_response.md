# 응답을 처리하려면?

## 세줄요약

+ WSGIRequestHandler 에서요청이 오면 handle(self) 함수를 호출하게 되는데,
+ 요청/응답을 정상적으로 만들면 handler.run() 을 호출해서 다음 과정을 거친다
+ 로우레벨 단의 소켓요청에 대해 finish를 수행한다

## 1. `wsgiref.handlers` 에서 처리

```python
class BaseHandler:
    """Manage the invocation of a WSGI application"""

    def run(self, application):
        """ Invoke the application. 앱을 "호출" 한다!
        (중략)
        """
        try:
            self.setup_environ()    # request 에 대한 환경변수 세팅
            self.result = application(self.environ, self.start_response)    # application 결과값 로드
            self.finish_response()  # iterable 데이터를 리턴하고, iterable 과 self를 닫는다.
        except (ConnectionAbortedError, BrokenPipeError, ConnectionResetError):
            # We expect the client to close the connection abruptly from time
            # to time.
            return
        except:
            try:
            except:
```

---

### 1.1. self.finish_response() 설명

1. file 형식의 리턴인지, 확인 파일 전송(이 구현체는, WSGI를 사용하는 다른 구현체들이 오버라이드 필요)인지 확인

+ 요청이 오면 handle을 돌 것이다

2. finish_response에서, body내의 값을 다음과 같이 처리한다
    list 내의 tuple을 꺼내와서[2 추가 읽기]
    처리 후 finish_content 수행 (헤더와 컨텐츠가 제대로 전송되었는지 확인)

3. 요청때 처리한 WSGIRequestHandler 처리가 끝난다.

### 1.2. sockerserver.py 에서 응답값을 전달

1. 모든 요청에 대해 해석하면 L7단에서 L4단으로 처리 레벨이 내려가고 패킷을 리턴할 것이다.
    1. finish_request()를 호출하고
    2. shutdown_request() 를 호출한다
        패킷을 닫음

2. 이 뒤에 serve_forever() 함수 - make_server 로 오픈한 서버 - 에 대해 request 를 셧다운한다. [4 추가-1]
    1. ready 라는 플래그를 통해 오픈된 서버에 대해 처리한다
    2. 플래그가 `set` 되면 `_handle_request_noblock` 이란 함수를 타고 서비스를 마무리한다

```python
(중략)
finally:
    self.__shutdown_request = False
    self.__is_shut_down.set()
```

---

2 추가
    1. 모던 클라이언트 (HTTP/0.9) 이상인지 체크
    2. 헤더 전송
        1. 헤더에 아래 내용을 추가함

        ```python
        def send_preamble(self):
            """Transmit version/status/date/server, via self._write()"""
            if self.origin_server:
                if self.client_is_modern():
                    self._write(('HTTP/%s %s\r\n' % (self.http_version,self.status)).encode('iso-8859-1'))
                    if 'Date' not in self.headers:
                        self._write(
                            ('Date: %s\r\n' % format_date_time(time.time())).encode('iso-8859-1')
                        )
                    if self.server_software and 'Server' not in self.headers:
                        self._write(('Server: %s\r\n' % self.server_software).encode('iso-8859-1'))
            else:
                self._write(('Status: %s\r\n' % self.status).encode('iso-8859-1'))
        ```

작업하면서 ServerHandler 라는 변수에 값을 계속해서 추가한다.
    여기서 서버 타입이나 시간값 등의 정보를 헤더에 추가한다

---
4 추가-1

serve_forever 구현체는 아래와 같다

    ```python
    def serve_forever(self, poll_interval=0.5):
        """Handle one request at a time until shutdown.

        Polls for shutdown every poll_interval seconds. Ignores
        self.timeout. If you need to do periodic tasks, do them in
        another thread.
        """
        self.__is_shut_down.clear()
        try:
            # XXX: Consider using another file descriptor or connecting to the
            # socket to wake this up instead of polling. Polling reduces our
            # responsiveness to a shutdown request and wastes cpu at all other
            # times.
            with _ServerSelector() as selector:
                selector.register(self, selectors.EVENT_READ)

                while not self.__shutdown_request:
                    ready = selector.select(poll_interval)
                    # bpo-35017: shutdown() called during select(), exit immediately.
                    if self.__shutdown_request:
                        break
                    if ready:
                        self._handle_request_noblock()

                    self.service_actions()
        finally:
            self.__shutdown_request = False
            self.__is_shut_down.set()
    ```

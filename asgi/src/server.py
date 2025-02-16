import asyncio
from typing import Callable


class MyAsgiProtocol(asyncio.Protocol):
    def __init__(self, app: Callable):
        self.app = app
        self.transport = None
        self._buffer = b''

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data: bytes):
        self._buffer += data

        if b"\r\n\r\n" in self._buffer:
            asyncio.create_task(self.handle_request())

    def connection_lost(self, exc):
        if exc:
            print(f"Connection lost: {exc}")
        else:
            print(f"Connection closed")

    async def handle_request(self):
        request_data = self._buffer.decode()

        # HTTP 요청 자체를 헤더, 바디로 파싱
        headers, _, body = request_data.partition("\r\n\r\n")

        # HTTP 요청 첫 줄 파싱 (예: "GET / HTTP/1.1")
        request_line, *_ = headers.split("\r\n")
        # HTTP method와 경로를 파싱
        method, path, _ = request_line.split(" ")

        scope = {
            "type": "http",
            "method": method,
            "path": path,
            "headers": [],  # 헤더를 추가할 수 있음
        }

        async def receive():
            """ 애플리케이션이 클라이언트로부터 메시지를 받게 해줌

            :return:
            """
            return {"type": "http.request", "body": body.encode(), "more_body": False}

        async def send(message):
            """ 애플리케이션이 이벤트 메시지를 클라이언트에 전송해줌

            :param message:
            :return:
            """
            if message["type"] == "http.response.start":
                response_headers = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"
                self.transport.write(response_headers)
            elif message["type"] == "http.response.body":
                self.transport.write(message["body"])
                self.transport.close()  # 응답 완료 후 연결 종료

        await self.app(scope, receive, send)

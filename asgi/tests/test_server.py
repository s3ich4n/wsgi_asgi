import asyncio

import aiohttp
import pytest

from src.application import app
from src.server import MyAsgiProtocol


@pytest.fixture
async def server():
    """서버 fixture: 테스트용 서버를 시작하고 정리"""
    loop = asyncio.get_event_loop()
    server = await loop.create_server(
        lambda: MyAsgiProtocol(app),
        "127.0.0.1",
        8000
    )

    try:
        await asyncio.sleep(0.1)
        yield server
    finally:
        server.close()
        await server.wait_closed()


@pytest.fixture
async def client():
    """클라이언트 fixture: aiohttp 클라이언트 세션 생성 및 정리"""
    async with aiohttp.ClientSession() as session:
        yield session


@pytest.mark.asyncio
async def test_get_request_returns_hello_world(server, client):
    """기본 HTTP GET 요청 테스트"""
    async with client.get("http://127.0.0.1:8000") as response:
        assert response.status == 200
        text = await response.text()
        assert text == "Hello, World!"


@pytest.mark.asyncio
async def test_post_request_returns_hello_world(server, client):
    """기본 HTTP POST 요청 테스트"""
    async with client.post("http://127.0.0.1:8000", data="Hello, ASGI!") as response:
        assert response.status == 200
        text = await response.text()
        assert text == "Hello, ASGI!"

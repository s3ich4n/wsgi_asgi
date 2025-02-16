async def app(scope, receive, send):
    """ ASGI 프로토콜 서버에서 데이터를 받고, 이를 가공

    :param scope:
    :param receive:
    :param send:
    :return:
    """
    if scope["method"] == "POST":
        request = await receive()
        body = request.get("body", b"")  # 요청 데이터 가져오기
    else:
        body = b"Hello, World!"  # GET 요청에서는 바디가 필요 없음

    await send(
        {
            'type': 'http.response.start',
            'status': 200,
            'headers': [
                [b'content-type', b'text/plain'],
            ],
        }
    )
    await send(
        {
            'type': 'http.response.body',
            'body': body,
        }
    )

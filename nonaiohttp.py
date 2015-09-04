import asyncio


@asyncio.coroutine
def echo_server():
    yield from asyncio.start_server(handle_connection, 'localhost', 8080)


@asyncio.coroutine
def handle_connection(reader, writer):
    buf = b''
    pattern1 = b'GET /test/1234 HTTP/1.1\r\nHost: localhost:8080\r\n\r\n'
    pattern2 = b'GET /test/1234 HTTP/1.0\r\nHost: localhost:8080\r\nUser-Agent: ApacheBench/2.3\r\nAccept: */*\r\n\r\n'
    pattern = pattern1
    while True:
        data = yield from reader.read(8192)
        if not data:
            return
        buf += data
        # print('data', data)
        # print('buf', buf)
        while buf.startswith(b'GET '):
            # print("answer")
            # print('.', end='')
            pos = buf.find(b'\r\n\r\n')
            buf = buf[pos+4:]
            answer = (b"HTTP/1.1 200 OK\r\n"
                      b"Content-Length: 6\r\n"
                      b"\r\n"
                      b"Answer")
            writer.write(answer)
        # print("remaining buffer", buf)


loop = asyncio.get_event_loop()
loop.run_until_complete(echo_server())
try:
    loop.run_forever()
finally:
    loop.close()
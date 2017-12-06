import argparse
import uuid
import json
import tempfile

from aiohttp import web
import aiohttp

from . import flow


# All front ws connected.
allws = {}


def parse_command_line():
    parser = argparse.ArgumentParser(description='Start server')

    parser.add_argument('-H', '--host', action='store', default='0.0.0.0',
                        help='Server host (default: 0.0.0.0)')

    parser.add_argument('-P', '--port', action='store', type=int, default=4444,
                        help='Server port (default: 4444)')

    args = parser.parse_args()
    return args


async def handle_flow(request):
    reader = await request.multipart()
    r = await reader.next()
    filename = r.filename

    # TODO: only hold chunk of file in memory, and send chunk to file to
    # websockets.
    #https://aiohttp.readthedocs.io/en/stable/web.html#file-uploads
    size = 0
    with tempfile.TemporaryFile() as f:
        while True:
            chunk = await r.read_chunk()
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

        f.seek(0)
        flow_output = f.read().decode()

    errors = flow.extract_errors(flow_output)
    data = json.dumps(errors)
    for ws in allws.values():
        await ws.send_str(data);
    return web.Response(text='ok')


async def websocket_handler(request):
    print('websocket_handler')
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    wsid = uuid.uuid4()
    allws[wsid] = ws

    async for msg in ws:
        print('message')
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
                allws.pop(wsid)
            else:
                print('Received: ', msg.data)
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print(f'ws connection closed with exception {ws.exception()}')
            allws.pop(wsid)

    print('websocket connection closed')
    allws.pop(wsid)

    return ws


def main():
    args = parse_command_line()

    app = web.Application()

    app.router.add_get('/ws', websocket_handler)
    app.router.add_post('/flow', handle_flow)

    web.run_app(app, host=args.host, port=args.port)

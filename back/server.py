import argparse
from aiohttp import web
import aiohttp


def parse_command_line():
    parser = argparse.ArgumentParser(description='Start server')

    parser.add_argument('-H', '--host', action='store', default='0.0.0.0',
                        help='Server host (default: 0.0.0.0)')

    parser.add_argument('-P', '--port', action='store', type=int, default=4444,
                        help='Server port (default: 4444)')

    args = parser.parse_args()
    return args


async def flow(request):
    data = await request.post()
    f = data['file'].file
    content = f.read()
    print(type(content), content)
    #import pdb; pdb.set_trace()
    return web.Response(text='ok')


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                print('Received: ', msg.data)
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print(f'ws connection closed with exception {ws.exception()}')

    print('websocket connection closed')

    return ws


def main():
    args = parse_command_line()

    app = web.Application()

    app.router.add_get('/ws', websocket_handler)
    app.router.add_post('/flow', flow)

    web.run_app(app, host=args.host, port=args.port)

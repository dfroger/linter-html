import argparse
import asyncio
import sys

import aiohttp
from aiohttp import FormData


def parse_command_line():
    parser = argparse.ArgumentParser(description='Upload linter warnings')

    parser.add_argument('-H', '--host', action='store', default='0.0.0.0',
                        help='Server host (default: 0.0.0.0)')

    parser.add_argument('-P', '--port', action='store', type=int, default=4444,
                        help='Server port (default: 4444)')

    parser.add_argument('--flow', action='store',
                        help='Upload flow warnings file')

    args = parser.parse_args()
    return args


async def upload_flow(base_url, fn):
    files = {
        'file': open(fn, 'rb')
    }
    url = f'{base_url}/flow'

    async with aiohttp.ClientSession() as session:
        await session.post(url, data=files)


def main():
    args = parse_command_line()

    base_url = f'http://{args.host}:{args.port}'

    if args.flow:
        upload = upload_flow(base_url, args.flow)
    else:
        print('nothing to do')
        sys.exit(1)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(upload)
    loop.close()

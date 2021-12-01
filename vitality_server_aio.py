import time
from aiohttp import web
import ssl
import asyncio
import vitality_poller_aio

async def handle(request):
    return web.json_response( await vitality_poller_aio.poll_all() )

app = web.Application()
app.add_routes([web.get('/poll_all', handle) ])


ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain('certs/server/cert.pem', 'certs/server/key.pem',password='123456')



def run(port=443):
    web.run_app(app, ssl_context=ssl_context, port=port)


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

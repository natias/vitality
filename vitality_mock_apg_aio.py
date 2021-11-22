import time
from aiohttp import web
import ssl
import asyncio

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
  #  await asyncio.sleep(0.8)
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])


ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.load_cert_chain('certs/mock/cert.pem', 'certs/mock/key.pem')
ssl_context.load_verify_locations(cafile='certs/cert.pem')

web.run_app(app, ssl_context=ssl_context)

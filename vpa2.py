import asyncio
import aiohttp
import ssl
import time
import vitality_conf
import json


def load_conf():
    global __VITALITY_CONF__
    __VITALITY_CONF__=vitality_conf.get_conf()
#    print(__VITALITY_CONF__)




async def fetch(session, i, sslcontext):
    url = __VITALITY_CONF__.get('base_url_server_part')+__VITALITY_CONF__.get('base_url_path')+__VITALITY_CONF__.get('pus')[i]
    start_time = time.monotonic_ns()
    async with session.get(url, ssl=sslcontext) as response:
        t = await response.text()
        c = response.status
        e = time.monotonic_ns() - start_time 
        return (i,t,c, e)


async def fetch_all( loop):
    async with aiohttp.ClientSession(loop=loop, connector=aiohttp.TCPConnector(limit=500)) as session:
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH,cafile='certs/mock/cert.pem')
        ssl_context.check_hostname = False
        ssl_context.load_cert_chain(certfile='certs/cert.pem', keyfile='certs/myKey.pem')
        #ssl_context.load_verify_locations(cafile='certs/mock/cert.pem')
        results = await asyncio.gather(*[fetch(session, i,ssl_context) for i in range(len(__VITALITY_CONF__.get('pus')))], return_exceptions=True)
        return results


def poll_all():
    load_conf()
    loop = asyncio.get_event_loop()
    stata = loop.run_until_complete(fetch_all( loop))
    print(json.dumps(stata))

if __name__ == '__main__':
    poll_all()

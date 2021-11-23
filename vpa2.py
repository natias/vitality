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


async def on_request_start(session, trace_config_ctx, params):
    trace_config_ctx.start = asyncio.get_event_loop().time()

async def on_request_end(session, trace_config_ctx, params):
    elapsed = asyncio.get_event_loop().time() - trace_config_ctx.start
    print("Request took {}".format(elapsed))

async def on_dns_resolvehost_end(session, trace_config_ctx, params):
    trace_config_ctx.start_conn_create = asyncio.get_event_loop().time()

async def on_connection_create_end(session, trace_config_ctx, params):
    elapsed = asyncio.get_event_loop().time() - trace_config_ctx.start_conn_create
    print("estab conn took {}".format(elapsed))


async def fetch(session, i, sslcontext):
    url = __VITALITY_CONF__.get('base_url_server_part')+__VITALITY_CONF__.get('base_url_path')+__VITALITY_CONF__.get('pus')[i].get('url_specifier')
    start_time = time.monotonic_ns()
    try:
     async with session.get(url, ssl=sslcontext) as response:
        t = await response.text()
        c = response.status
        e = time.monotonic_ns() - start_time 
        return (i,t,c, e)
    except Exception as e:
     return (i,"error "+str(e),-1,time.monotonic_ns() - start_time) 


async def fetch_all( loop):
    trace_config = aiohttp.TraceConfig()
#    trace_config.on_dns_resolvehost_end.append(on_dns_resolvehost_end)
#    trace_config.on_connection_create_end.append(on_connection_create_end)
    trace_config.on_request_start.append(on_request_start)
    trace_config.on_request_end.append(on_request_end)
    async with aiohttp.ClientSession(loop=loop, connector=aiohttp.TCPConnector(limit=100),trace_configs=[trace_config]) as session:
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH,cafile='certs/mock/cert.pem')
        ssl_context.check_hostname = False
        ssl_context.load_cert_chain(certfile='certs/cert.pem', keyfile='certs/myKey.pem')
        #ssl_context.load_verify_locations(cafile='certs/mock/cert.pem')
        results = await asyncio.gather(*[fetch(session, i,ssl_context) for i in range(len(__VITALITY_CONF__.get('pus')))], return_exceptions=True)
        return results

def decide_status(stata):
    return "Healthy"

def calcTotalRespTime(stata):
    print(stata)
    return sum(e for a,b,c,e in stata)

def generate_result_list(stata):
    return "" 

def prepare_answer(stata):
    answer={}
    answer["applicationInfo"]=__VITALITY_CONF__.get('applicationInfo') 
    answer["status"]=decide_status(stata) 
    answer["totalResponseTime"]=calcTotalRespTime(stata)
    answer["results"]=generate_result_list(stata)
    return answer

def poll_all():
    load_conf()
    loop = asyncio.get_event_loop()
    stata = loop.run_until_complete(fetch_all( loop))
    print((stata))
    answer=prepare_answer(stata)
    return(json.dumps(answer))

if __name__ == '__main__':
    print(poll_all())

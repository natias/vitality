import time
import requests
from requests_pkcs12 import Pkcs12Adapter
import asyncio
from timeit import default_timer
from concurrent.futures import ThreadPoolExecutor
import vitality_conf



def load_conf():
    global __VITALITY_CONF__
    __VITALITY_CONF__=vitality_conf.get_conf()
    print(__VITALITY_CONF__)

#for now i just make sure that the response
def validate_resp(response):
    if response.status_code == 200 and len(response.text)> 10:
        return 0
    else:
        return 1

def request(session, i):
#    url = "https://localhost:8443/abcdefghij"
    url = __VITALITY_CONF__.get('base_url')+__VITALITY_CONF__.get('pus')[i]
    headers = {
    }
    try:
     with session.get(url,headers=headers, timeout=(0.6,0.95),verify=False) as response:
#        data = response.text
#
#        if response.status_code != 200:
#            print("FAILURE::{0}".format(url))
#
#        elapsed_time = default_timer() - START_TIME
#        completed_at = "{:5.2f}s".format(elapsed_time)
        rv=validate_resp(response)
        return (i,rv)
    except requests.exceptions.ReadTimeout:
        return (i,2)
    except requests.exceptions.ConnectionError as e:
        print(e)
        return (i,3)

async def start_async_process():
    x=[-1]*len(__VITALITY_CONF__.get('pus'))
    with ThreadPoolExecutor(max_workers=50) as executor:
        with requests.Session() as session:
            adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
            session.mount('https://',adapter)
            session.mount('https://example.com', Pkcs12Adapter(pkcs12_filename='certs/keyStore.p12', pkcs12_password='123456'))
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    request,
                    *(session,i)
                )
                for i in range(len(__VITALITY_CONF__.get('pus')))
            ]
            for response in await asyncio.gather(*tasks):
               (j,d)=response
               x[j]=d
    return x


def poll_all():
    load_conf()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(start_async_process())
    loop.run_until_complete(future)
    return (future.result())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(start_async_process())
    loop.run_until_complete(future)
    print (future.result())

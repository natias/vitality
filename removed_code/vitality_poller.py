import time
import requests
#from requests_pkcs12 import Pkcs12Adapter
import asyncio
from timeit import default_timer
from concurrent.futures import ThreadPoolExecutor
import vitality_conf
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import vitality_client_ssl
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

requests.urllib3.disable_warnings()

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

#def request( i,session,conn_timeout,read_timeout)#,cert_file,cert_pass):
def request( i,session,conn_timeout,read_timeout):
#    url = "https://localhost:8443/abcdefghij"
#  with requests.Session() as session:
#    adapter = requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50)
#    session.mount('https://',adapter)
#    vitality_client_ssl.decorate_session_with_ssl(session,cert_file ,cert_pass)
    url = __VITALITY_CONF__.get('base_url_server_part')+__VITALITY_CONF__.get('base_url_path')+__VITALITY_CONF__.get('pus')[i]
    headers = {
    }
    try:
     with session.get(url,headers=headers, timeout=(conn_timeout,read_timeout),verify=False) as response:
        rv=validate_resp(response)
        return (i,rv)
    except requests.exceptions.ReadTimeout:
        return (i,2)
    except requests.exceptions.ConnectionError as e:
        print(e)
        return (i,3)




async def start_async_process(cert_pass):
    x=[-1]*len(__VITALITY_CONF__.get('pus'))
    conn_timeout=__VITALITY_CONF__.get('connection_time_out_seconds')
    read_timeout=__VITALITY_CONF__.get('read_time_out_seconds')
    cert_file=__VITALITY_CONF__.get('cert_file_path')
    with ThreadPoolExecutor(max_workers=500) as executor:
        with requests.Session() as session:
            adapter = requests.adapters.HTTPAdapter(pool_connections=500, pool_maxsize=500)
            session.mount('https://',adapter)
            vitality_client_ssl.decorate_session_with_ssl(session,cert_file ,cert_pass,500,500)         
            session.get(__VITALITY_CONF__.get('base_url_server_part'),verify=False)
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    request,
                    #*(i,session,conn_timeout,read_timeout,cert_file,cert_pass)
                    *(i,session,conn_timeout,read_timeout)
                )
                for i in range(len(__VITALITY_CONF__.get('pus')))
            ]
            for response in await asyncio.gather(*tasks):
               (j,d)=response
               x[j]=d
    return x


def poll_all(cert_pass):
    load_conf()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(start_async_process(cert_pass))
    loop.run_until_complete(future)
    return (future.result())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(start_async_process())
    loop.run_until_complete(future)
    print (future.result())

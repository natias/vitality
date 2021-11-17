import time
import requests
import asyncio
from timeit import default_timer
from concurrent.futures import ThreadPoolExecutor

START_TIME = default_timer()

def request(session, i):
    url = "https://jsonplaceholder.typicode.com/posts"
    headers = {
#          'Connection': 'close',
    }
    with session.get(url,headers=headers) as response:
        data = response.text

        if response.status_code != 200:
            print("FAILURE::{0}".format(url))

        elapsed_time = default_timer() - START_TIME
        completed_at = "{:5.2f}s".format(elapsed_time)
#        print("{0:<30} {1:>20}".format(i, completed_at))
        return (i,data)

async def start_async_process():
    print("{0:<30} {1:>20}".format("No", "Completed at"))
    x=[0]*150
    with ThreadPoolExecutor(max_workers=50) as executor:
        with requests.Session() as session:
            loop = asyncio.get_event_loop()
            START_TIME = default_timer()
            tasks = [
                loop.run_in_executor(
                    executor,
                    request,
                    *(session,i)
                )
                for i in range(150)
            ]
            for response in await asyncio.gather(*tasks):
#               print( response )
               (j,d)=response
               x[j]=len(d)
#               pass
    return x


def V():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(start_async_process())
    loop.run_until_complete(future)
    
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(start_async_process())
    loop.run_until_complete(future)
    print (future.result())

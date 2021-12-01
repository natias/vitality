from concurrent.futures import ThreadPoolExecutor
import aiohttp
import asyncio
import time
import ssl


async def request( i,session):
     pokemon_url = f'https://localhost:8443/okemon{number}'
     async with session.get(pokemon_url,ssl=False) as resp:
            pokemon = await resp.text()
            #print(pokemon)
            return (i,pokemon)


async def start_async_process():
    with ThreadPoolExecutor(max_workers=500) as executor:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64),trust_env=True) as session:
            
            ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH,cafile='certs/mock/cert.pem')
            ssl_context.check_hostname = False
            ssl_context.load_verify_locations(cafile='certs/mock/cert.pem')
     
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(
                    executor,
                    request,
                    *(i,session)
                )
                for i in range(100)
            ]
            for response in await asyncio.gather(*tasks):
               (j,d)=response
               x[j]=d
    return x



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(start_async_process())
    loop.run_until_complete(future)
    print (future.result())


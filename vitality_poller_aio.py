import aiohttp
import asyncio
import time
import ssl

start_time = time.time()


async def main():

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=64),trust_env=True) as session:

        for number in range(1, 1501):
            pokemon_url = f'https://localhost:8443/okemon{number}'
            ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH,cafile='certs/mock/cert.pem')
            ssl_context.check_hostname = False
            ssl_context.load_verify_locations(cafile='certs/mock/cert.pem')
            async with session.get(pokemon_url,ssl=False) as resp:
                pokemon = await resp.text()
                print(pokemon)

asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))


import asyncio
import nest_asyncio
from aiohttp import request
import aiofiles
from aiomultiprocess import Pool
import uvloop

nest_asyncio.apply()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}


async def get(u: str) -> None:
    async with request('GET', u, headers=HEADERS) as r:
        print('GET', u)
        if r.status == 200:
            filename = u.split('/')[-1]  # modify this as needed
            async with aiofiles.open(filename, 'wb') as f:
                await f.write(await r.read())
        else:
            print(f'\u001b[31m Error:{r.status}\t{u}\u001b[0m')


async def main():
    urls: list = ['https://c8.alamy.com/comp/WWH9YM/siberia-husky-sled-dog-dogphoto-dog-photo-dog-photos-WWH9YM.jpg',
                  'https://thumbs.dreamstime.com/b/french-bulldog-small-breed-domestic-dog-were-result-s-cross-ancestors-imported-england-local-136021670.jpg',
                  'https://images.all-free-download.com/images/graphiclarge/cute_dog_photo_picture_7_168843.jpg']
    async with Pool(loop_initializer=uvloop.new_event_loop) as pool:
        await pool.map(get, urls)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

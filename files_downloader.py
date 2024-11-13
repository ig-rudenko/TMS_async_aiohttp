import asyncio
import time
from random import random, choice

import aiohttp
import requests

COUNT = 50
URL = "https://it-bookshelf.ru/media/previews/14/preview.png"


def download(url: str):
    res = requests.get(url)
    print(len(res.text))


async def download_async(url: str) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(response.status)

            # Синхронная нагрузка!!!!!
            # time.sleep(2)
            # ===================

            # Асинхронная нагрузка
            await asyncio.sleep(2)
            # ===================

            if random() < 0.5:
                raise choice((aiohttp.ClientError, aiohttp.ClientResponseError, ValueError))

            return len(await response.read())


async def run_async():
    s = time.perf_counter()
    tasks = []
    for i in range(COUNT):
        tasks.append(asyncio.create_task(download_async(URL)))

    res = await asyncio.gather(*tasks, return_exceptions=True)
    e = time.perf_counter()
    print(f"Асинхронное выполнение заняло {e - s} секунд")

    print(res)


def run_sync():
    s = time.perf_counter()
    for i in range(COUNT):
        download(URL)
    e = time.perf_counter()
    print(f"Синхронное выполнение заняло {e - s} секунд")


if __name__ == '__main__':
    # run_sync()
    asyncio.run(run_async())

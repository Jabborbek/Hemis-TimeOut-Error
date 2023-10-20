import asyncio
import time

import aiohttp


async def get_request_page_count(url: str, header):
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.get(url=url) as response:
            datas = await response.json()
            return datas['data']['pagination']['pageCount']


async def fetch_data_optimized(url, header=None, semaphore=None):
    async with semaphore:
        time_out = aiohttp.ClientTimeout(total=60 * 2)
        start_time = time.time()
        try:
            async with aiohttp.ClientSession(headers=header, timeout=time_out,
                                             connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.get(url) as response:
                    data = await response.json()
                    for res in data['data']['items']:
                        pass
                    execution_time = time.time() - start_time
                    print(f"{url.split('=')[-1]}: page is fetched in {execution_time:.2f} seconds")
                    return data
        except asyncio.TimeoutError:
            print(f"Timeout error occurred while fetching page {url.split('=')[-1]}. Retrying...")
            await asyncio.sleep(5)
            return await fetch_data_optimized(url, header, semaphore)  # rekursiv qayta urinish


async def student_job():
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Authorization": f"Bearer ssdfsfdsfd-dqdqddffd-fwefwefd",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Connection": "keep-alive",
    }
    base_url = "https://student.otm.uz/rest/v1/data/student-list?limit=50"
    pages_count = await get_request_page_count(url=base_url, header=header)
    urls = [f"{base_url}&page={page}" for page in range(1, pages_count + 1)]
    semaphore = asyncio.Semaphore(10)
    tasks = [fetch_data_optimized(url, header=header, semaphore=semaphore) for url in urls]
    await asyncio.gather(*tasks)
    print('Finished')

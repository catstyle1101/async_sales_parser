import asyncio
import json
from typing import NamedTuple

import aiohttp
import tqdm

from config import BASE_URL, BASE_DOMAIN, LOGIN, PASSWORD, MAN_ID


class DatesOfDocuments(NamedTuple):
    date_begin: str
    date_end: str


async def _fetch(url: str, session: aiohttp.ClientSession, semaphore, headers, to_json) -> dict | str:
    async with semaphore:
        async with session.get(url, headers=headers) as response:
            body = await response.text()
            if to_json:
                result = json.loads(body)
                return result
            else:
                return body


async def _scrap_list_of_urls(urls: list[str], to_json) -> list[str]:
    SEMAPHORE_VALUE = 200
    headers = {
        'authority': BASE_DOMAIN,
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'user-agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'),
        'x-requested-with': 'XMLHttpRequest',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'referer': f'{BASE_URL}cat/invoice.html',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        }
    sem = asyncio.Semaphore(SEMAPHORE_VALUE)
    async with aiohttp.ClientSession(headers=headers) as session:
        result = await session.get(f'{BASE_URL}ns2000/data-login.php?'
                                   f't=login&log={LOGIN}&pwd={PASSWORD}&retPath='
                                   f'/ipro2/login?&_=1661929993479',
                                   allow_redirects=True)
        res = json.loads(await result.text())
        headers['cookie'] = f'login={LOGIN}; man-id={MAN_ID}; session-id={res.get("session")}'

        tasks = list()
        for url in urls:
            tasks.append(asyncio.ensure_future(_fetch(url, session, sem, headers, to_json)))
        if to_json:
            bar_name = "Ищу документы в базе"
        else:
            bar_name = "Проверяю документы администраторов"
        result = [await f for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks), desc=bar_name)]
        return result


def scrap_urls(urls: list[str], to_json=True):
    """Main function for async scrapping data."""
    loop = asyncio.get_event_loop()
    future = _scrap_list_of_urls(urls, to_json)
    result = loop.run_until_complete(future)
    return result

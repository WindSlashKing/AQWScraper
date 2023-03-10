from bs4 import BeautifulSoup
import httpx

import json
import os
import asyncio

CLIENT = httpx.AsyncClient()

BASE_URL = "https://zeroaq.com/library/wiki/datatables/quests"

BASE_QUEST_URL = "https://zeroaq.com/wiki/quest/"

RESULTS_PER_PAGE = 100

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "utf-8",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "https://zeroaq.com",
    "Connection": "keep-alive",
    "Referer": "https://zeroaq.com/wiki",
    "Cookie": "ci_session=ucegov7i8qqqt5llpl6qepd11nlroh94",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers"
}

async def scrape_no_requirements_quests():
    ids: set[str] = await get_all_pages_ids()
    print(f"Got all {len(ids)} quest IDs")
    links = construct_links(ids)
    print(f"Constructed all {len(links)} links")
    
    no_requirements: dict[str, str] = dict()
    
    tasks = set()
    for link in links:
        task = asyncio.ensure_future(check_has_requirements(link))
        tasks.add(task)

    responses = await asyncio.gather(*tasks)
    for has_requirements, quest_name, link in responses:
        if not has_requirements:
            no_requirements[quest_name] = link

    save_results(os.path.join("scraped_data", "zeroaq.json"), no_requirements)
    
def save_results(filename, results: dict[str, str]):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

async def get_quest_ids(page: int) -> set[str]:
    
    payload = f"draw={page + 3}&columns[0][data]=0&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=1&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&order[0][column]=0&order[0][dir]=asc&start={page * RESULTS_PER_PAGE}&length={RESULTS_PER_PAGE}&search[value]=&search[regex]=false"

    response = await CLIENT.post(BASE_URL, data=payload, headers=HEADERS)
    ids: set[str] = set()

    if '"data": []' in response.text:
        return ids

    json_data = response.json()
    quest_objects = json_data["data"]
    for quest in quest_objects:
        ids.add(quest["-1"])
    return ids

async def get_all_pages_ids() -> set[str]:
    ids: set[str] = set()
    for page in range(0, 9999999):
        new_ids = await get_quest_ids(page)
        if not new_ids:
            print(f"No new ids. Stopping search at page: {page}")
            return ids
        ids.update(new_ids)
    return ids

def construct_links(ids: set[str]) -> set[str]:
    return set([BASE_QUEST_URL + id for id in ids])

async def check_has_requirements(link: str):
    print(f"Checking link: {link}")
    response = await CLIENT.get(link, headers=HEADERS)
    if len(response.text) < 500:
        print("Something went wrong with check_has_requirements")
        print(response.text)
        raise ConnectionError
    soup = BeautifulSoup(response.text, "html.parser")
    match = soup.find("div", class_="card-header")
    quest_name = "Unknown"
    if len(match.text) > 1:
        quest_name = match.get_text().strip()
    has_requirements = "requirement" in response.text.lower()
    return (has_requirements, quest_name, link)
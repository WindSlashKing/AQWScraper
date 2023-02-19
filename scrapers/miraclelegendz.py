from bs4 import BeautifulSoup
import httpx

import json
import os

CLIENT = httpx.Client()

BASE_URL = "https://miraclelegendz.online/wiki/quests"

BASE_QUEST_URL = "https://miraclelegendz.online/wiki/quest/"

RESULTS_PER_PAGE = 100

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
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

def scrape_no_requirements_quests():
    ids: set[str] = get_all_pages_ids()
    print(f"Got all {len(ids)} quest IDs")
    links = construct_links(ids)
    print(f"Constructed all {len(links)} links")
    
    no_requirements: dict[str, str] = dict()
    
    for link in links:
        print(f"Checking link: {link}")
        (has_requirements, quest_name) = check_has_requirements(link)
        if not has_requirements:
            no_requirements[quest_name] = link

    save_results(os.path.join("scraped_data", "miraclelegendz.json"), no_requirements)
    
def save_results(filename, results: dict[str, str]):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f)

def get_quest_ids(page: int) -> set[str]:
    
    payload = f"draw={page + 3}&columns[0][data]=0&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=1&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&order[0][column]=0&order[0][dir]=asc&start={page * RESULTS_PER_PAGE}&length={RESULTS_PER_PAGE}&search[value]=&search[regex]=false"

    response = CLIENT.post(BASE_URL, data=payload, headers=HEADERS)
    ids: set[str] = set()

    if '"data": []' in response.text:
        return ids

    json_data = response.json()
    quest_objects = json_data["data"]
    for quest in quest_objects:
        ids.add(quest[0])
    return ids

def get_all_pages_ids() -> set[str]:
    ids: set[str] = set()
    for page in range(0, 9999999):
        new_ids = get_quest_ids(page)
        if not new_ids:
            print(f"No new ids. Stopping search at page: {page}")
            return ids
        ids.update(new_ids)
    return ids

def construct_links(ids: set[str]) -> set[str]:
    return set([BASE_QUEST_URL + id for id in ids])

def check_has_requirements(link: str):
    response = CLIENT.get(link, headers=HEADERS)
    if len(response.text) < 500:
        print("Something went wrong with check_has_requirements")
        print(response.text)
        raise ConnectionError
    soup = BeautifulSoup(response.text, "html.parser")
    match = soup.find("p", class_="card-text")
    quest_name = "Unknown"
    if len(match.text) > 1:
        quest_name = match.get_text().strip()
    
    requirement_links = soup.find_all("a", href=True)
    has_requirements = False
    for link in requirement_links:
        if "wiki/item/" in link["href"]:
            has_requirements = True 
            break

    return (has_requirements, quest_name)
from bs4 import BeautifulSoup
import json
from constants import *

def get_quest_ids(page: int) -> set[str]:
    
    payload = f"draw={page + 3}&columns[0][data]=0&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=1&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&order[0][column]=0&order[0][dir]=asc&start={page * RESULTS_PER_PAGE}&length={RESULTS_PER_PAGE}&search[value]=&search[regex]=false"

    response = CLIENT.post(BASE_URL, data=payload, headers=HEADERS)
    ids: set[str] = set()

    if '"data": []' in response.text:
        return ids

    json_data = response.json()
    quest_objects = json_data["data"]
    for quest in quest_objects:
        ids.add(quest["-1"])
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
    match = soup.find("div", class_="card-header")
    quest_name = "Unknown"
    if len(match.text) > 1:
        quest_name = match.get_text().strip()
    has_requirements = "requirement" in response.text.lower()
    return (has_requirements, quest_name)
    
def main():
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
    
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(no_requirements, f)

if __name__ == "__main__":
    main()
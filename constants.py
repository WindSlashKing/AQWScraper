import httpx

CLIENT = httpx.Client()

BASE_URL = "https://zeroaq.com/library/wiki/datatables/quests"

BASE_QUEST_URL = "https://zeroaq.com/wiki/quest/"

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
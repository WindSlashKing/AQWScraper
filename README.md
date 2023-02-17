# AQWScraper
A simple script to scape data from zeroaq.com and miraclelegendz.online.
The script uses httpx and beautifulsoup to scrape all quests that do not have any requirements.
Quests don't change over time so speed does not matter. That is why the code is not asynchronous.
The json library is used to save the data to a file.

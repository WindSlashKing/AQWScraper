import asyncio

import scrapers.zeroaq as zeroaq
import scrapers.asworld as asworld

async def main():

    print("(1) Scrape zeroaq.com")
    print("(2) Scrape as-world.org")
    choice = input("> ")
    
    if "1" in choice:
        await zeroaq.scrape_no_requirements_quests()
    elif "2" in choice:
        await asworld.scrape_no_requirements_quests()
    else:
        print("Invalid input")
        input("Press enter to exit...")
        return

    print("Done!")

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.get_event_loop().run_until_complete(main())
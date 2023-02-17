import zeroaq
import miraclelegendz

def main():

    print("(1) Scrape zeroaq.com")
    print("(2) Scrape miraclelegendz.online")
    choice = input("> ")
    
    if "1" in choice:
        zeroaq.scrape_no_requirements_quests()
    elif "2" in choice:
        miraclelegendz.scrape_no_requirements_quests()
    else:
        print("Invalid input")
        input("Press enter to exit...")
        return

    print("Done!")

if __name__ == "__main__":
    main()
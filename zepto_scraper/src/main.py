from scraper import ZeptoScraper
from parser import ZeptoParser


def main():

    url = input("Enter Zepto Product URL: ").strip()

    scraper = ZeptoScraper()

    try:

        scraper.start()

        html, api_data = scraper.scrape(url)

        parser = ZeptoParser()

        product = parser.parse(api_data)

        print("\n========== PRODUCT ==========")

        for key, value in product.items():

            print(f"{key}: {value}")

    finally:

        scraper.close()


if __name__ == "__main__":
    main()
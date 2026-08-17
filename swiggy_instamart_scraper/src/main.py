from scraper import InstamartScraper
from parser import parse_product
from exporter import export_to_csv


def main():

    scraper = InstamartScraper()

    try:
        scraper.start_browser()

        print("Browser started successfully")

        url = input("Enter URL: ").strip()

        scraper.open_page(url)

        html = scraper.get_page_source()

        product = parse_product(html)

        product["url"] = url

        print("\n===== PRODUCT DATA =====")

        for key, value in product.items():
            print(f"{key}: {value}")

        export_to_csv(product)

        input("\nPress ENTER to close browser...")

    finally:
        scraper.close()


if __name__ == "__main__":
    main()
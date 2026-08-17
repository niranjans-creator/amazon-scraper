
from pathlib import Path

from .scraper import scrape_product
from .parser import parse_product
from .csv_export import export_to_csv


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# ============================================================
# MAIN SCRAPER
# ============================================================

def main():

    # --------------------------------------------------------
    # PRODUCT URL
    # --------------------------------------------------------

    url = input(
        "\nEnter Blinkit product URL: "
    ).strip()

    if not url:
        print("No URL provided.")
        return

    print("\n" + "=" * 60)
    print("Starting Blinkit product scraper")
    print("=" * 60)

    print(f"\nURL: {url}")

    try:

        # ----------------------------------------------------
        # SCRAPE PAGE
        # ----------------------------------------------------

        print("\nOpening Blinkit product page...")

        scraped_data = scrape_product(url)

        if not scraped_data:
            print("\nNo data was returned from the scraper.")
            return

        # ----------------------------------------------------
        # PARSE PRODUCT
        # ----------------------------------------------------

        print("\nParsing product information...")

        product = parse_product(
            scraped_data
        )

        if not product:
            print("\nCould not parse product information.")
            return

        # ----------------------------------------------------
        # DISPLAY PRODUCT INFORMATION
        # ----------------------------------------------------

        print("\n" + "=" * 60)
        print("PRODUCT INFORMATION")
        print("=" * 60)

        print(
            f"\nTitle: {product.title}"
        )

        print(
            f"Brand: {product.brand}"
        )

        print(
            f"Product ID: {product.product_id}"
        )

        print(
            f"Price: {product.price}"
        )

        print(
            f"Weight: {product.weight}"
        )

        print(
            f"Category: {product.category}"
        )

        print(
            f"Description: {product.description}"
        )

        print(
            f"Images found: "
            f"{len(product.images_url) if product.images_url else 0}"
        )

        # ----------------------------------------------------
        # EXPORT CSV
        # ----------------------------------------------------

        print("\nCreating CSV file...")

        csv_file = export_to_csv(
            product
        )

        print("\n" + "=" * 60)
        print("SCRAPING COMPLETED")
        print("=" * 60)

        print(
            f"\nCSV saved to:\n{csv_file}"
        )

    except Exception as error:

        print("\n" + "=" * 60)
        print("SCRAPING ERROR")
        print("=" * 60)

        print(
            f"\n{type(error).__name__}: {error}"
        )


# ============================================================
# RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()


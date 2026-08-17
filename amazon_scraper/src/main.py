from api import get_product_data
from csv_export import save_to_csv
import re


def extract_asin(url):
    """Extract ASIN from an Amazon product URL."""
    patterns = [
        r"/dp/([A-Z0-9]{10})",
        r"/gp/product/([A-Z0-9]{10})",
        r"/product/([A-Z0-9]{10})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError("Invalid Amazon Product URL")


def parse_product(data, url):
    product = data.get("product", {})

    return {
        "Product Title": product.get("title", ""),
        "Description": product.get("description", ""),
        "Weight": product.get("weight", ""),
        "Category": product.get("categories_flat", ""),
        "Images":product.get("images_flat", []),
        "Price": product.get("buybox_winner", {}).get("price", {}).get("value", ""),
        "URL": url,
        "Ingredients": product.get("ingredients", ""),
        "Nutritional Facts": product.get("nutritional_facts", "")
    }


def main():
    amazon_url = input("Enter Amazon Product URL:\n")

    try:
        asin = extract_asin(amazon_url)
        print(f"\nASIN: {asin}")

        data = get_product_data(asin)

        if not data:
            print("Failed to fetch product data.")
            return

        product = parse_product(data, amazon_url)

        print("\n===== PRODUCT DETAILS =====")
        for key, value in product.items():
            print(f"{key}: {value}")

        save_to_csv(product)

        print("\nCSV exported successfully!")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
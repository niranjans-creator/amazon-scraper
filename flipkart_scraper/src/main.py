import os
import sys
import csv
from datetime import datetime

from flask import Flask, render_template, request, jsonify, send_file

# Make src imports work
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from scraper import open_product
from parser import parse_product


app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates")
)


# Folder where scraped CSV files will be saved
SCRAPED_FOLDER = os.path.join(BASE_DIR, "scraped_products")

os.makedirs(SCRAPED_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scrape", methods=["POST"])
def scrape():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data received."
            }), 400

        url = data.get("url", "").strip()

        if not url:
            return jsonify({
                "success": False,
                "error": "Please enter a Flipkart product URL."
            }), 400

        if "flipkart.com" not in url.lower():
            return jsonify({
                "success": False,
                "error": "Please enter a valid Flipkart URL."
            }), 400

        print("\n================ SCRAPING ================")
        print(f"URL: {url}")

        # Open Flipkart and capture HTML
        html = open_product(url)

        if not html:
            return jsonify({
                "success": False,
                "error": "Failed to retrieve the Flipkart page."
            }), 500

        print("\n================ PARSING ================")

        # Parse product information
        product = parse_product(html)

        if not product:
            return jsonify({
                "success": False,
                "error": "Could not extract product information."
            }), 500

        print("\n================ PRODUCT ================")

        for key, value in product.items():
            print(f"{key}: {value}")

        # Save CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = f"product_{timestamp}.csv"
        filepath = os.path.join(SCRAPED_FOLDER, filename)

        save_product_to_csv(product, filepath)

        print("\n================ EXPORT ================")
        print(f"CSV saved to: {filepath}")

        return jsonify({
            "success": True,
            "product": product,
            "filename": filename
        })

    except Exception as e:
        print("\nSCRAPER ERROR:")
        print(str(e))

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


def save_product_to_csv(product, filepath):
    """
    Save one scraped product to CSV.
    """

    # Keep a consistent column order
    fieldnames = [
        "title",
        "description",
        "weight",
        "image_url",
        "category",
        "price",
        "ingredients",
        "nutritional_facts"
    ]

    with open(
        filepath,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        row = {}

        for field in fieldnames:
            value = product.get(field, "")

            # Convert lists to readable text
            if isinstance(value, list):
                value = " | ".join(str(item) for item in value)

            row[field] = value

        writer.writerow(row)


@app.route("/download/<filename>")
def download(filename):

    filepath = os.path.join(
        SCRAPED_FOLDER,
        filename
    )

    if not os.path.exists(filepath):
        return "File not found.", 404

    return send_file(
        filepath,
        as_attachment=True,
        download_name=filename
    )


if __name__ == "__main__":
    print("\n========================================")
    print("       FLIPKART SCRAPER WEB APP")
    print("========================================")
    print("\nOpen this in your browser:")
    print("http://127.0.0.1:5000")
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
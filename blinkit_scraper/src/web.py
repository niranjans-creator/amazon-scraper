from flask import Flask, render_template, request, send_file, jsonify
from pathlib import Path

from .scraper import scrape_product
from .parser import parse_product
from .csv_export import export_to_csv


# ============================================================
# FLASK APP
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

app = Flask(
    __name__,
    template_folder=str(PROJECT_ROOT / "templates")
)


# ============================================================
# DIRECTORIES
# ============================================================

SCRAPED_PRODUCTS_DIR = PROJECT_ROOT / "scraped products"

SCRAPED_PRODUCTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
# SCRAPE PRODUCT
# ============================================================

@app.route("/scrape", methods=["POST"])
def scrape():

    try:

        # ----------------------------------------------------
        # GET URL FROM FRONTEND
        # ----------------------------------------------------

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
                "error": "Please enter a Blinkit product URL."
            }), 400

        print("\n" + "=" * 60)
        print("Starting scrape:")
        print(url)
        print("=" * 60)

        # ----------------------------------------------------
        # SCRAPE BLINKIT
        # ----------------------------------------------------

        scraped_data = scrape_product(url)

        if not scraped_data:

            return jsonify({
                "success": False,
                "error": "Failed to scrape the Blinkit page."
            }), 500

        # ----------------------------------------------------
        # PARSE PRODUCT
        #
        # IMPORTANT:
        # parse_product() accepts ONE argument.
        # ----------------------------------------------------

        product = parse_product(scraped_data)

        if not product:

            return jsonify({
                "success": False,
                "error": "Could not extract product information."
            }), 500

        # ----------------------------------------------------
        # DISPLAY PRODUCT INFORMATION
        # ----------------------------------------------------

        print("\nProduct information:")
        print(f"Title: {product.title}")
        print(f"Brand: {product.brand}")
        print(f"Product ID: {product.product_id}")
        print(f"Price: {product.price}")
        print(f"Weight: {product.weight}")
        print(f"Category: {product.category}")
        print(f"Description: {product.description}")
        print(f"Images found: {len(product.images_url or [])}")

        # ----------------------------------------------------
        # CREATE SAFE CSV FILE NAME
        # ----------------------------------------------------

        product_title = (
            product.title
            or "blinkit_product"
        )

        safe_title = "".join(
            character
            for character in product_title
            if character.isalnum()
            or character in (" ", "-", "_")
        )

        safe_title = (
            safe_title
            .strip()
            .replace(" ", "_")
        )

        if not safe_title:
            safe_title = "blinkit_product"

        filename = f"{safe_title}.csv"

        output_path = (
            SCRAPED_PRODUCTS_DIR /
            filename
        )

        # ----------------------------------------------------
        # EXPORT CSV
        # ----------------------------------------------------

        print("\nCreating CSV file...")

        export_to_csv(
            product,
            str(output_path)
        )

        print("\nCSV saved to:")
        print(output_path.resolve())

        # ----------------------------------------------------
        # RETURN PRODUCT TO FRONTEND
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "message": "Product scraped successfully.",

            "product": {

                "product_id":
                    product.product_id,

                "title":
                    product.title,

                "brand":
                    product.brand,

                "description":
                    product.description,

                "category":
                    product.category,

                "price":
                    product.price,

                "weight":
                    product.weight,

                "images_url":
                    product.images_url,

                "ingredients":
                    product.ingredients,

                "nutritional_facts":
                    product.nutritional_facts
            },

            "filename":
                filename,

            "download_url":
                f"/download/{filename}"
        })

    except Exception as error:

        print("\nWeb scraping error:")
        print(error)

        return jsonify({

            "success": False,

            "error": str(error)

        }), 500


# ============================================================
# DOWNLOAD CSV
# ============================================================

@app.route("/download/<filename>")
def download(filename):

    try:

        # ----------------------------------------------------
        # PREVENT PATH TRAVERSAL
        # ----------------------------------------------------

        requested_file = Path(filename)

        if (
            requested_file.name != filename
            or ".." in requested_file.parts
        ):

            return jsonify({
                "error": "Invalid file name."
            }), 400

        file_path = (
            SCRAPED_PRODUCTS_DIR /
            filename
        )

        # ----------------------------------------------------
        # CHECK FILE
        # ----------------------------------------------------

        if not file_path.exists():

            return jsonify({
                "error": "CSV file not found."
            }), 404

        # ----------------------------------------------------
        # DOWNLOAD
        # ----------------------------------------------------

        return send_file(
            file_path,
            as_attachment=True,
            download_name=file_path.name,
            mimetype="text/csv"
        )

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("BLINKIT SCRAPER WEB APP")
    print("=" * 60)

    print()
    print("Open your browser:")
    print("http://127.0.0.1:5000")
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
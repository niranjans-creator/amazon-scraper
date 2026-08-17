import csv
from pathlib import Path


def export_to_csv(product, filename=None):
    """
    Save one scraped product to a CSV file.

    The CSV will be saved inside:
    scraped products/
    """

    project_root = Path(__file__).resolve().parent.parent

    output_folder = project_root / "scraped products"
    output_folder.mkdir(parents=True, exist_ok=True)

    if filename is None:
        filename = "flipkart_products.csv"

    output_file = output_folder / filename

    # Keep the column order consistent
    fields = [
        "title",
        "description",
        "weight",
        "image_url",
        "category",
        "price",
        "ingredients",
        "nutritional_facts",
    ]

    with open(output_file, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=fields,
            extrasaction="ignore"
        )

        writer.writeheader()
        writer.writerow(product)

    print(f"\nCSV saved successfully:")
    print(output_file)

    return str(output_file)
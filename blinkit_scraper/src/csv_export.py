
import csv
from pathlib import Path


# ============================================================
# EXPORT PRODUCT TO CSV
# ============================================================

def export_to_csv(product, filename=None):
    """
    Export one scraped product to CSV.

    If filename is provided:
        Save the CSV to that location.

    Otherwise:
        Save it inside the 'scraped products' folder
        using the product title as the filename.
    """

    # --------------------------------------------------------
    # DEFAULT OUTPUT LOCATION
    # --------------------------------------------------------

    if filename is None:

        project_root = (
            Path(__file__)
            .resolve()
            .parent
            .parent
        )

        output_directory = (
            project_root / "scraped products"
        )

        output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        # ----------------------------------------------------
        # PRODUCT TITLE
        # ----------------------------------------------------

        title = getattr(
            product,
            "title",
            ""
        )

        if not title:
            title = "blinkit_product"

        # ----------------------------------------------------
        # MAKE SAFE FILENAME
        # ----------------------------------------------------

        safe_title = "".join(
            character
            for character in title
            if character.isalnum()
            or character in (
                " ",
                "-",
                "_"
            )
        )

        safe_title = (
            safe_title
            .strip()
            .replace(
                " ",
                "_"
            )
        )

        if not safe_title:
            safe_title = "blinkit_product"

        filename = (
            output_directory
            / f"{safe_title}.csv"
        )

    else:

        filename = Path(
            filename
        )

        filename.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    # --------------------------------------------------------
    # PRODUCT DATA
    # --------------------------------------------------------

    images = getattr(
        product,
        "images_url",
        []
    )

    # Store all image URLs in one CSV cell
    images_text = "\n".join(
        images
    ) if images else ""

    row = {

        "Product ID": getattr(
            product,
            "product_id",
            ""
        ),

        "Title": getattr(
            product,
            "title",
            ""
        ),

        "Brand": getattr(
            product,
            "brand",
            ""
        ),

        "Description": getattr(
            product,
            "description",
            ""
        ),

        "Category": getattr(
            product,
            "category",
            ""
        ),

        "Price": getattr(
            product,
            "price",
            ""
        ),

        "Weight": getattr(
            product,
            "weight",
            ""
        ),

        "Images URL": images_text,

        "Ingredients": getattr(
            product,
            "ingredients",
            ""
        ),

        "Nutritional Facts": getattr(
            product,
            "nutritional_facts",
            ""
        )
    }

    # --------------------------------------------------------
    # WRITE CSV
    # --------------------------------------------------------

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=row.keys()
        )

        writer.writeheader()

        writer.writerow(
            row
        )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    absolute_path = Path(
        filename
    ).resolve()

    print(
        "\nCSV created successfully:"
    )

    print(
        absolute_path
    )

    return str(
        absolute_path
    )


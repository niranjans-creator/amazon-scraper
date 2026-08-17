import pandas as pd
from pathlib import Path


def export_to_csv(product):
    output_dir = Path("scraped_products")
    output_dir.mkdir(exist_ok=True)

    df = pd.DataFrame([{
        "title": product.title,
        "brand": product.brand,
        "price": product.price,
        "mrp": product.mrp,
        "weight": product.weight,
        "description": product.description,
        "ingredients": product.ingredients,
        "category": product.category,
        "image_urls": ", ".join(product.image_urls),
        "product_url": product.product_url
    }])

    file_path = output_dir / "products.csv"

    df.to_csv(file_path, index=False)

    print(f"\nCSV saved to: {file_path}")
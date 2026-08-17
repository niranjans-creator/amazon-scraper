import pandas as pd
from pathlib import Path


def export_to_csv(product):

    output_dir = Path("scraped products")
    output_dir.mkdir(exist_ok=True)

    csv_file = output_dir / "products.csv"

    df = pd.DataFrame([product])

    if csv_file.exists():
        df.to_csv(
            csv_file,
            mode="a",
            header=False,
            index=False,
            encoding="utf-8-sig"
        )
    else:
        df.to_csv(
            csv_file,
            index=False,
            encoding="utf-8-sig"
        )

    print(f"\nCSV saved to: {csv_file}")
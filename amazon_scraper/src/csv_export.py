import csv

def save_to_csv(product, filename="products.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=product.keys())
        writer.writeheader()
        writer.writerow(product)

    print(f"✅ CSV saved as {filename}")
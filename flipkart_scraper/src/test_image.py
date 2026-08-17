from parser import parse_product


HTML_FILE = "output/flipkart_product.html"


with open(
    HTML_FILE,
    "r",
    encoding="utf-8"
) as f:
    html = f.read()


product = parse_product(html)


print("\n========== RAW IMAGE URL ==========\n")

print(repr(product["image_url"]))


print("\n========== SPLIT IMAGES ==========\n")

images = product["image_url"].split(" | ")

for i, image in enumerate(images, 1):

    print(f"IMAGE {i}:")
    print(repr(image))
    print()
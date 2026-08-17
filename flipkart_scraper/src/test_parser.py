import os

from parser import parse_product


def main():

    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    html_file = os.path.join(
        project_root,
        "output",
        "flipkart_product.html"
    )

    with open(
        html_file,
        "r",
        encoding="utf-8"
    ) as file:

        html = file.read()

    product = parse_product(html)

    print("\n================ PRODUCT ================\n")

    for key, value in product.items():

        print(f"{key}:")
        print(value)
        print("\n-----------------------------------------\n")


if __name__ == "__main__":
    main()
import os
import re
from bs4 import BeautifulSoup


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

    soup = BeautifulSoup(html, "html.parser")

    # Get all visible text
    text = soup.get_text(" ", strip=True)

    keywords = [
        "ingredient",
        "ingredients",
        "nutrition",
        "nutritional",
        "energy",
        "protein",
        "carbohydrate",
        "carbohydrates",
        "fat",
        "fiber",
        "dietary fiber",
        "serving size",
        "net quantity",
        "quantity",
        "weight"
    ]

    print("\n========== KEYWORD SEARCH ==========\n")

    for keyword in keywords:

        matches = list(
            re.finditer(
                re.escape(keyword),
                text,
                re.IGNORECASE
            )
        )

        print(f"{keyword}: {len(matches)} occurrence(s)")

        for match in matches[:3]:

            start = max(0, match.start() - 250)
            end = min(
                len(text),
                match.end() + 500
            )

            print("\n--- Context ---")
            print(text[start:end])
            print()


if __name__ == "__main__":
    main()
    
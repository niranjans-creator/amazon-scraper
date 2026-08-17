from bs4 import BeautifulSoup
import os


def inspect_page():
    project_root = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    html_file = os.path.join(
        project_root,
        "output",
        "flipkart_product.html"
    )

    if not os.path.exists(html_file):
        print("ERROR: flipkart_product.html was not found.")
        return

    with open(html_file, "r", encoding="utf-8") as file:
        html = file.read()

    print(f"HTML loaded: {len(html)} characters")

    soup = BeautifulSoup(html, "html.parser")

    print("\n===== PAGE TITLE =====")

    if soup.title:
        print(soup.title.get_text(" ", strip=True))
    else:
        print("Not found")

    print("\n===== H1 TAGS =====")

    h1_tags = soup.find_all("h1")

    if h1_tags:
        for h1 in h1_tags:
            text = h1.get_text(" ", strip=True)

            if text:
                print(text)
    else:
        print("No H1 tags found")

    print("\n===== META DESCRIPTION =====")

    meta = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if meta:
        print(meta.get("content", ""))
    else:
        print("Not found")

    print("\n===== JSON-LD BLOCKS =====")

    scripts = soup.find_all(
        "script",
        attrs={"type": "application/ld+json"}
    )

    print(f"Found {len(scripts)} JSON-LD blocks")

    for i, script in enumerate(scripts, start=1):

        print(f"\n--- JSON-LD {i} ---")

        text = script.string

        if text:
            print(text[:5000])


if __name__ == "__main__":
    inspect_page()
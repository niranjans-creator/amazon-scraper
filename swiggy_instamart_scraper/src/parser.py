from bs4 import BeautifulSoup
import json
import re


def extract_weight(text):

    if not text:
        return ""

    patterns = [
        r'(\d+(?:\.\d+)?\s*kg)',
        r'(\d+(?:\.\d+)?\s*g)',
        r'(\d+(?:\.\d+)?\s*gm)',
        r'(\d+(?:\.\d+)?\s*ml)',
        r'(\d+(?:\.\d+)?\s*l)'
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return ""


def parse_product(html):

    soup = BeautifulSoup(html, "lxml")

    product = {}

    scripts = soup.find_all("script")

    for script in scripts:

        if not script.string:
            continue

        try:

            text = script.string.strip()

            if '"@type": "Product"' not in text:
                continue

            data = json.loads(text)

            product["title"] = data.get("name", "")

            brand = data.get("brand", {})
            product["brand"] = brand.get("name", "")

            offers = data.get("offers", {})

            product["price"] = offers.get("price", "")

            product["availability"] = offers.get(
                "availability",
                ""
            )

            images = data.get("image", [])

            if isinstance(images, list):
                product["image_urls"] = " | ".join(images)
            else:
                product["image_urls"] = images

            break

        except Exception:
            continue

    # Description
    meta_desc = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if meta_desc:
        product["description"] = meta_desc.get(
            "content",
            ""
        )
    else:
        product["description"] = ""

    # Try title first
    weight = extract_weight(
        product.get("title", "")
    )

    # If not found, try description
    if not weight:
        weight = extract_weight(
            product.get("description", "")
        )

    product["weight"] = weight

    return product
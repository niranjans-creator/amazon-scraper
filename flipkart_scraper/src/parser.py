import json
import re
from bs4 import BeautifulSoup


def clean_image_url(url):
    """
    Convert a Flipkart/Markdown-style image URL into a plain URL.

    Example:
    [https://example.com/test.jpg?q=70](https://example.com/test.jpg?q=70)

    becomes:
    https://example.com/test.jpg?q=70
    """

    if not url:
        return ""

    url = str(url).strip()

    # Markdown format:
    # [display text](actual URL)
    match = re.search(r"\]\((https?://[^)]+)\)", url)

    if match:
        return match.group(1)

    # Sometimes the URL itself is wrapped in []
    if url.startswith("[") and url.endswith("]"):
        url = url[1:-1].strip()

    return url


def clean_image_urls(images):
    """
    Clean a list of image URLs.

    Also handles:
    - Markdown URLs
    - Plain URLs
    - Multiple URLs separated by |
    """

    if not images:
        return []

    if isinstance(images, str):
        # Split multiple images if they are stored in one string
        images = images.split("|")

    cleaned = []

    for image in images:
        image = clean_image_url(image)

        if image and image not in cleaned:
            cleaned.append(image)

    return cleaned


def extract_json_ld(soup):
    """
    Extract Product JSON-LD data from the Flipkart page.
    """

    scripts = soup.find_all(
        "script",
        type="application/ld+json"
    )

    for script in scripts:
        try:
            data = json.loads(script.string or script.get_text())

            # JSON-LD can be a list
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("@type") == "Product":
                        return item

            # Or a dictionary
            if isinstance(data, dict):
                if data.get("@type") == "Product":
                    return data

                # Sometimes @graph contains Product
                graph = data.get("@graph", [])

                if isinstance(graph, list):
                    for item in graph:
                        if (
                            isinstance(item, dict)
                            and item.get("@type") == "Product"
                        ):
                            return item

        except (json.JSONDecodeError, TypeError):
            continue

    return {}


def extract_weight(text):
    """
    Extract product weight from page text.

    Examples:
    1 kg
    1KG
    500 g
    500gm
    2.5 kg
    """

    if not text:
        return ""

    patterns = [
        r"\b(\d+(?:\.\d+)?)\s*(kg|kgs|kilogram|kilograms)\b",
        r"\b(\d+(?:\.\d+)?)\s*(g|gm|gms|gram|grams)\b",
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)

        if matches:
            value, unit = matches[0]

            unit = unit.lower()

            if unit in ["kg", "kgs", "kilogram", "kilograms"]:
                return f"{value} KG"

            return f"{value} G"

    return ""


def extract_price(product_data, text):
    """
    Extract the current product price.
    """

    offers = product_data.get("offers", {})

    if isinstance(offers, dict):
        price = offers.get("price")

        if price:
            return price

    # Fallback: search page text
    matches = re.findall(
        r"(?:₹|Rs\.?)\s*([\d,]+(?:\.\d+)?)",
        text,
        re.IGNORECASE
    )

    if matches:
        # Usually the first relevant price is the product price
        return matches[0].replace(",", "")

    return ""


def extract_category(product_data, soup):
    """
    Extract product category.
    """

    category = product_data.get("category")

    if category:
        return str(category).strip()

    # Fallback from breadcrumb
    text = soup.get_text(" ", strip=True)

    if "Flour" in text:
        return "flour"

    return ""


def extract_ingredients(text):
    """
    Try to find ingredients from the page.

    Flipkart does not always expose ingredients in JSON-LD,
    so this searches the page text.
    """

    if not text:
        return ""

    patterns = [
        r"ingredients?\s*[:\-]\s*(.{0,1000})",
        r"composition\s*[:\-]\s*(.{0,1000})",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            value = match.group(1)

            # Stop at common section names
            value = re.split(
                r"\b(nutrition|nutritional|directions|storage|benefits|shelf life)\b",
                value,
                flags=re.IGNORECASE
            )[0]

            value = value.strip(" :-|")

            if value:
                return value

    return ""


def extract_nutritional_facts(text):
    """
    Try to extract nutritional information from the page.
    """

    if not text:
        return ""

    nutrition_keywords = [
        "energy",
        "protein",
        "carbohydrate",
        "carbohydrates",
        "total fat",
        "fat",
        "fiber",
        "fibre",
        "sugar",
        "sodium",
    ]

    found = []

    for keyword in nutrition_keywords:

        pattern = rf"\b{re.escape(keyword)}\b\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?\s*(?:g|gm|mg|kcal|kcalories|%)?)"

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        for value in matches:
            item = f"{keyword.title()}: {value}"

            if item not in found:
                found.append(item)

    return " | ".join(found)


def parse_product(html):
    """
    Main product parser.

    Input:
        HTML string

    Output:
        Product dictionary
    """

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    # Full page text
    page_text = soup.get_text(
        " ",
        strip=True
    )

    # Product JSON-LD
    product_data = extract_json_ld(soup)

    # -------------------------
    # TITLE
    # -------------------------

    title = product_data.get("name", "")

    if not title:
        h1 = soup.find("h1")

        if h1:
            title = h1.get_text(
                " ",
                strip=True
            )

    if not title:
        title = soup.title.get_text(
            " ",
            strip=True
        ) if soup.title else ""

    # -------------------------
    # DESCRIPTION
    # -------------------------

    description = product_data.get(
        "description",
        ""
    )

    # -------------------------
    # IMAGES
    # -------------------------

    images = product_data.get(
        "image",
        []
    )

    if isinstance(images, str):
        images = [images]

    images = clean_image_urls(images)

    # -------------------------
    # CATEGORY
    # -------------------------

    category = extract_category(
        product_data,
        soup
    )

    # -------------------------
    # PRICE
    # -------------------------

    price = extract_price(
        product_data,
        page_text
    )

    # -------------------------
    # WEIGHT
    # -------------------------

    weight = extract_weight(
        page_text
    )

    # -------------------------
    # INGREDIENTS
    # -------------------------

    ingredients = extract_ingredients(
        page_text
    )

    # -------------------------
    # NUTRITION
    # -------------------------

    nutritional_facts = extract_nutritional_facts(
        page_text
    )

    # -------------------------
    # RETURN PRODUCT
    # -------------------------

    return {
        "title": title,
        "description": description,
        "weight": weight,
        "image_url": " | ".join(images),
        "category": category,
        "price": price,
        "ingredients": ingredients,
        "nutritional_facts": nutritional_facts,
    }
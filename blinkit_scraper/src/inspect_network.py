import json
from pathlib import Path


KEYWORDS = [
    "product",
    "product_id",
    "productId",
    "name",
    "title",
    "brand",
    "price",
    "mrp",
    "weight",
    "image",
    "description",
    "category",
    "ingredient",
    "nutrition",
    "nutritional",
]


def search_value(value, path="root"):

    results = []

    if isinstance(value, dict):

        for key, item in value.items():

            key_lower = str(key).lower()

            if any(
                keyword.lower() in key_lower
                for keyword in KEYWORDS
            ):

                results.append(
                    (f"{path}.{key}", item)
                )

            results.extend(
                search_value(
                    item,
                    f"{path}.{key}"
                )
            )

    elif isinstance(value, list):

        for index, item in enumerate(value):

            results.extend(
                search_value(
                    item,
                    f"{path}[{index}]"
                )
            )

    return results


def main():

    file_path = Path(
        "output/network_data.json"
    )

    if not file_path.exists():

        print(
            "ERROR: output/network_data.json "
            "was not found."
        )

        print(
            "Run the Blinkit scraper first."
        )

        return

    print("Loading network data...")

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    print(
        f"Loaded {len(data)} network responses."
    )

    print(
        "\nSearching for product fields..."
    )

    found = []

    for index, response in enumerate(
        data,
        start=1
    ):

        response_data = response.get(
            "data"
        )

        if not response_data:
            continue

        matches = search_value(
            response_data,
            f"response[{index}]"
        )

        if matches:

            found.append(
                (
                    index,
                    response.get("url"),
                    matches
                )
            )

    print(
        f"\nResponses containing relevant "
        f"fields: {len(found)}"
    )

    for response_index, url, matches in found:

        print("\n")
        print("=" * 80)
        print(
            f"RESPONSE {response_index}"
        )
        print("=" * 80)

        print("\nURL:")
        print(url)

        print("\nMATCHES:")

        printed = set()

        for path, value in matches:

            identifier = (
                path,
                repr(value)
            )

            if identifier in printed:
                continue

            printed.add(identifier)

            print(f"\n{path}")

            if isinstance(
                value,
                (dict, list)
            ):

                formatted = json.dumps(
                    value,
                    indent=2,
                    ensure_ascii=False
                )

                print(
                    formatted[:3000]
                )

            else:

                print(
                    repr(value)
                )


if __name__ == "__main__":
    main()
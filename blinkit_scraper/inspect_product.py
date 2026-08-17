import json
import sys


# Force UTF-8 output on Windows
sys.stdout.reconfigure(
    encoding="utf-8",
    errors="replace"
)


FILE = "output/product_response_9.json"


with open(
    FILE,
    "r",
    encoding="utf-8"
) as f:

    data = json.load(f)


KEYWORDS = [
    "product",
    "name",
    "title",
    "brand",
    "description",
    "category",
    "price",
    "mrp",
    "weight",
    "quantity",
    "image",
    "ingredient",
    "nutrition",
    "nutritional",
]


def inspect(value, path="root"):

    if isinstance(value, dict):

        for key, item in value.items():

            key_lower = str(key).lower()

            if any(
                keyword in key_lower
                for keyword in KEYWORDS
            ):

                print(
                    f"\n{path}.{key}:"
                )

                if isinstance(
                    item,
                    (dict, list)
                ):

                    text = json.dumps(
                        item,
                        indent=2,
                        ensure_ascii=False
                    )

                    print(
                        text[:3000]
                    )

                else:

                    print(
                        repr(item)
                    )

            inspect(
                item,
                f"{path}.{key}"
            )

    elif isinstance(value, list):

        for i, item in enumerate(value):

            inspect(
                item,
                f"{path}[{i}]"
            )


print("=" * 70)
print("BLINKIT PRODUCT RESPONSE INSPECTION")
print("=" * 70)

inspect(data)

print("\nInspection complete.")
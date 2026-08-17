import json
import sys

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


response = data.get("response", {})

snippets = response.get(
    "snippets",
    []
)


print("=" * 80)
print("BLINKIT PRODUCT SNIPPETS")
print("=" * 80)


for index, snippet in enumerate(snippets):

    snippet_text = json.dumps(
        snippet,
        ensure_ascii=False
    )

    # Only inspect snippets containing our product ID
    if "68482" not in snippet_text:
        continue

    print("\n")
    print("=" * 80)
    print(f"SNIPPET INDEX: {index}")
    print("=" * 80)

    print(
        json.dumps(
            snippet,
            indent=2,
            ensure_ascii=False
        )
    )
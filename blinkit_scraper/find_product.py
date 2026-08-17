import json

with open(
    "output/network_data.json",
    "r",
    encoding="utf-8"
) as file:
    data = json.load(file)


for index, response in enumerate(data, start=1):

    response_data = response.get("data", {})

    text = json.dumps(
        response_data,
        ensure_ascii=False
    )

    if "68482" in text:

        print("=" * 70)
        print(f"RESPONSE {index}")
        print("=" * 70)
        print("URL:")
        print(response.get("url"))

        print("\nProduct ID 68482 found.")

        # Save the complete matching response
        output_file = (
            f"output/product_response_{index}.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as output:

            json.dump(
                response_data,
                output,
                indent=2,
                ensure_ascii=False
            )

        print(
            f"Saved to: {output_file}"
        )
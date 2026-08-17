import json


class ZeptoParser:

    def parse(self, api_responses):

        product = {
            "title": "",
            "description": "",
            "weight": "",
            "category": "",
            "price": "",
            "ingredients": "",
            "image_urls": []
        }

        print(f"Responses captured: {len(api_responses)}")

        for response in api_responses:

            data = response.get("data")

            found = self.find_product_schema(data)

            if not found:
                continue

            print("FOUND PRODUCT!")

            product["title"] = found.get("name", "")
            product["description"] = found.get("description", "")
            product["category"] = found.get("category", "")
            product["weight"] = found.get("size", "")
            product["image_urls"] = found.get("image", [])

            offers = found.get("offers", {})
            product["price"] = offers.get("price", "")

            for item in found.get("additionalProperty", []):

                if item.get("name", "").lower() == "ingredients":
                    product["ingredients"] = item.get("value", "")

            return product

        return product

    def find_product_schema(self, obj):

        if isinstance(obj, str):

            if '"@type":"Product"' in obj or '"@type": "Product"' in obj:

                try:
                    return json.loads(obj)
                except:
                    return None

            return None

        if isinstance(obj, dict):

            if obj.get("@type") == "Product":
                return obj

            for value in obj.values():

                result = self.find_product_schema(value)

                if result:
                    return result

        elif isinstance(obj, list):

            for item in obj:

                result = self.find_product_schema(item)

                if result:
                    return result

        return None
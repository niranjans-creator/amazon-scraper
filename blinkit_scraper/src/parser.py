
import re
from dataclasses import dataclass, field
from urllib.parse import urlparse


# ============================================================
# PRODUCT DATA MODEL
# ============================================================

@dataclass
class Product:
    product_id: str = ""
    title: str = ""
    brand: str = ""
    description: str = ""
    category: str = ""
    price: str = ""
    weight: str = ""
    images_url: list = field(default_factory=list)
    ingredients: str = ""
    nutritional_facts: str = ""


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(value):
    if value is None:
        return ""

    if isinstance(value, str):
        return re.sub(r"\s+", " ", value).strip()

    return str(value).strip()


# ============================================================
# RECURSIVE SEARCH
# ============================================================

def find_values(obj, key):
    results = []

    if isinstance(obj, dict):

        for current_key, value in obj.items():

            if str(current_key).lower() == key.lower():
                results.append(value)

            results.extend(
                find_values(value, key)
            )

    elif isinstance(obj, list):

        for item in obj:

            results.extend(
                find_values(item, key)
            )

    return results


# ============================================================
# EXTRACT PRODUCT ID FROM URL
# ============================================================

def get_product_id_from_url(url):
    """
    Extract Blinkit product ID from:

    https://blinkit.com/prn/product-name/prid/539734
    """

    if not url:
        return ""

    match = re.search(
        r"/prid/(\d+)",
        url,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return ""


# ============================================================
# FIND PRODUCT ID
# ============================================================

def find_product_id(data, target_product_id=""):
    """
    Prefer the product ID supplied by the URL.
    """

    if target_product_id:
        return target_product_id

    possible_keys = [
        "product_id",
        "productId",
        "id"
    ]

    for key in possible_keys:

        values = find_values(
            data,
            key
        )

        for value in values:

            if value is None:
                continue

            value = clean_text(value)

            if value:
                return value

    return ""


# ============================================================
# CHECK WHETHER OBJECT BELONGS TO PRODUCT
# ============================================================

def object_belongs_to_product(obj, product_id):
    """
    Check whether a dictionary contains the target
    Blinkit product ID.
    """

    if not isinstance(obj, dict):
        return False

    if not product_id:
        return False

    possible_keys = [
        "product_id",
        "productId",
        "productID",
        "id"
    ]

    for key in possible_keys:

        value = obj.get(key)

        if value is not None:

            if str(value) == str(product_id):
                return True

    return False


# ============================================================
# FIND PRODUCT OBJECTS
# ============================================================

def find_product_objects(obj, product_id):
    """
    Recursively find dictionaries that belong to
    the requested Blinkit product.
    """

    results = []

    if isinstance(obj, dict):

        if object_belongs_to_product(
            obj,
            product_id
        ):
            results.append(obj)

        for value in obj.values():

            results.extend(
                find_product_objects(
                    value,
                    product_id
                )
            )

    elif isinstance(obj, list):

        for item in obj:

            results.extend(
                find_product_objects(
                    item,
                    product_id
                )
            )

    return results


# ============================================================
# FIND TITLE
# ============================================================

def find_title(data, product_id=""):

    product_objects = find_product_objects(
        data,
        product_id
    )

    possible_keys = [
        "product_name",
        "productName",
        "title",
        "name"
    ]

    # First search target product objects
    for obj in product_objects:

        for key in possible_keys:

            value = obj.get(key)

            if isinstance(value, str):

                value = clean_text(value)

                if value and len(value) > 2:
                    return value

    # Fallback
    for key in possible_keys:

        values = find_values(
            data,
            key
        )

        for value in values:

            if isinstance(value, str):

                value = clean_text(value)

                if value and len(value) > 2:
                    return value

    return ""


# ============================================================
# FIND BRAND
# ============================================================

def find_brand(data, product_id=""):

    product_objects = find_product_objects(
        data,
        product_id
    )

    for obj in product_objects:

        value = obj.get("brand")

        if isinstance(value, str):

            value = clean_text(value)

            if value:
                return value

        if isinstance(value, dict):

            name = value.get("name")

            if name:
                return clean_text(name)

    # Fallback
    values = find_values(
        data,
        "brand"
    )

    for value in values:

        if isinstance(value, str):

            value = clean_text(value)

            if value:
                return value

    return ""


# ============================================================
# FIND DESCRIPTION
# ============================================================

def find_description(data, product_id=""):
    """
    Blinkit product descriptions are commonly stored inside:

    attributes
        -> name = Description
        -> attribute_name = Description
        -> value = actual description

    We search the target product object first.
    """

    product_objects = find_product_objects(
        data,
        product_id
    )

    # --------------------------------------------------------
    # Search target product objects
    # --------------------------------------------------------

    for obj in product_objects:

        attributes = obj.get("attributes")

        if not isinstance(attributes, list):
            continue

        for attribute in attributes:

            if not isinstance(attribute, dict):
                continue

            name = clean_text(
                attribute.get("name")
            ).lower()

            attribute_name = clean_text(
                attribute.get("attribute_name")
            ).lower()

            if (
                name == "description"
                or attribute_name == "description"
                or "description" in name
                or "description" in attribute_name
            ):

                value = attribute.get("value")

                if isinstance(value, str):

                    value = clean_text(value)

                    if value:
                        return value

                value_info = attribute.get(
                    "value_info"
                )

                if isinstance(value_info, list):

                    for item in value_info:

                        if not isinstance(item, dict):
                            continue

                        value = item.get("value")

                        if isinstance(value, str):

                            value = clean_text(value)

                            if value:
                                return value

    # --------------------------------------------------------
    # Search ALL attributes as fallback
    # --------------------------------------------------------

    attributes_lists = find_values(
        data,
        "attributes"
    )

    for attributes in attributes_lists:

        if not isinstance(attributes, list):
            continue

        for attribute in attributes:

            if not isinstance(attribute, dict):
                continue

            name = clean_text(
                attribute.get("name")
            ).lower()

            attribute_name = clean_text(
                attribute.get("attribute_name")
            ).lower()

            if (
                name == "description"
                or attribute_name == "description"
            ):

                value = attribute.get("value")

                if isinstance(value, str):

                    value = clean_text(value)

                    if value:
                        return value

                value_info = attribute.get(
                    "value_info"
                )

                if isinstance(value_info, list):

                    for item in value_info:

                        if isinstance(item, dict):

                            value = item.get("value")

                            if isinstance(value, str):

                                value = clean_text(value)

                                if value:
                                    return value

    return ""


# ============================================================
# FIND WEIGHT
# ============================================================

def find_weight(data, product_id=""):

    product_objects = find_product_objects(
        data,
        product_id
    )

    possible_keys = [
        "unit",
        "weight",
        "quantity",
        "pack_size"
    ]

    # Search target product
    for obj in product_objects:

        for key in possible_keys:

            value = obj.get(key)

            if isinstance(value, str):

                value = clean_text(value)

                if re.search(
                    r"\d+(?:\.\d+)?\s*(kg|g|gm|mg|ml|l|litre|liter)",
                    value,
                    re.IGNORECASE
                ):
                    return value

        attributes = obj.get("attributes")

        if isinstance(attributes, list):

            for attribute in attributes:

                if not isinstance(attribute, dict):
                    continue

                name = clean_text(
                    attribute.get("name")
                ).lower()

                if name in (
                    "unit",
                    "weight",
                    "quantity",
                    "pack size"
                ):

                    value = attribute.get("value")

                    if value:
                        return clean_text(value)

    return ""


# ============================================================
# FIND CATEGORY
# ============================================================

def find_category(data, product_id=""):

    product_objects = find_product_objects(
        data,
        product_id
    )

    for obj in product_objects:

        categories = obj.get("categories")

        if not isinstance(categories, dict):
            continue

        names = []

        for key in (
            "L0Cat",
            "L1Cat",
            "L2Cat"
        ):

            category = categories.get(key)

            if isinstance(category, dict):

                name = clean_text(
                    category.get("Name")
                )

                if name:
                    names.append(name)

        if names:
            return " > ".join(names)

    return ""


# ============================================================
# FIND PRICE
# ============================================================

def find_price(data, product_id=""):

    product_objects = find_product_objects(
        data,
        product_id
    )

    # --------------------------------------------------------
    # Search target product objects
    # --------------------------------------------------------

    for obj in product_objects:

        normal_price = obj.get(
            "normal_price"
        )

        if isinstance(normal_price, dict):

            text = normal_price.get(
                "text"
            )

            if isinstance(text, str):

                match = re.search(
                    r"[\d,]+(?:\.\d+)?",
                    text
                )

                if match:

                    number = match.group(
                        0
                    ).replace(",", "")

                    if float(number) > 0:
                        return number

        price = obj.get("price")

        if isinstance(
            price,
            (int, float)
        ) and price > 0:

            return str(price)

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    prices = find_values(
        data,
        "price"
    )

    for price in prices:

        if isinstance(
            price,
            (int, float)
        ) and price > 0:

            return str(
                int(price)
                if float(price).is_integer()
                else price
            )

        if isinstance(price, str):

            match = re.search(
                r"\d+(?:\.\d+)?",
                price
            )

            if match:

                number = float(
                    match.group(0)
                )

                if number > 0:

                    return str(
                        int(number)
                        if number.is_integer()
                        else number
                    )

    return ""


# ============================================================
# CHECK IMAGE URL
# ============================================================

def is_image_url(value):

    if not isinstance(value, str):
        return False

    value = clean_text(value)

    if not value.startswith("http"):
        return False

    return bool(
        re.search(
            r"\.(jpg|jpeg|png|webp)(?:\?|$)",
            value,
            re.IGNORECASE
        )
    )


# ============================================================
# FIND PRODUCT IMAGES
# ============================================================

def find_images(data, product_id=""):
    """
    IMPORTANT:

    Only collect images from dictionaries belonging to
    the requested product.

    This prevents images from recommended products,
    similar products and other Blinkit products from
    being included.
    """

    images = []

    # --------------------------------------------------------
    # Find only objects belonging to requested product
    # --------------------------------------------------------

    product_objects = find_product_objects(
        data,
        product_id
    )

    for obj in product_objects:

        # -----------------------------------------------
        # Direct "images" field
        # -----------------------------------------------

        image_values = obj.get(
            "images"
        )

        if isinstance(image_values, list):

            for image in image_values:

                if is_image_url(image):

                    image = clean_text(image)

                    if image not in images:
                        images.append(image)

        # -----------------------------------------------
        # image_url
        # -----------------------------------------------

        for key in (
            "image_url",
            "imageUrl",
            "image"
        ):

            value = obj.get(key)

            if is_image_url(value):

                value = clean_text(value)

                if value not in images:
                    images.append(value)

    # --------------------------------------------------------
    # Search nested image data INSIDE target objects
    # --------------------------------------------------------

    for obj in product_objects:

        nested_images = find_values(
            obj,
            "images"
        )

        for value in nested_images:

            if isinstance(value, list):

                for image in value:

                    if is_image_url(image):

                        image = clean_text(image)

                        if image not in images:
                            images.append(image)

    return images


# ============================================================
# FIND INGREDIENTS
# ============================================================

def find_ingredients(data, product_id=""):

    product_objects = find_product_objects(
        data,
        product_id
    )

    for obj in product_objects:

        attributes = obj.get(
            "attributes"
        )

        if not isinstance(attributes, list):
            continue

        for attribute in attributes:

            if not isinstance(attribute, dict):
                continue

            name = clean_text(
                attribute.get("name")
            ).lower()

            attribute_name = clean_text(
                attribute.get("attribute_name")
            ).lower()

            if (
                "ingredient" in name
                or "ingredient" in attribute_name
            ):

                value = attribute.get(
                    "value"
                )

                if isinstance(value, str):

                    value = clean_text(value)

                    if value:
                        return value

    return ""


# ============================================================
# FIND NUTRITIONAL FACTS
# ============================================================

def find_nutritional_facts(
    data,
    product_id=""
):

    product_objects = find_product_objects(
        data,
        product_id
    )

    possible_keys = [
        "nutritional_facts",
        "nutrition",
        "nutritionalFacts",
        "nutrients"
    ]

    for obj in product_objects:

        for key in possible_keys:

            value = obj.get(key)

            if isinstance(value, str):

                value = clean_text(value)

                if value:
                    return value

            if isinstance(
                value,
                (dict, list)
            ):

                return str(value)

        attributes = obj.get(
            "attributes"
        )

        if isinstance(attributes, list):

            for attribute in attributes:

                if not isinstance(attribute, dict):
                    continue

                name = clean_text(
                    attribute.get("name")
                ).lower()

                attribute_name = clean_text(
                    attribute.get("attribute_name")
                ).lower()

                if (
                    "nutrition" in name
                    or "nutritional" in name
                    or "nutrition" in attribute_name
                    or "nutritional" in attribute_name
                ):

                    value = attribute.get(
                        "value"
                    )

                    if value:

                        if isinstance(
                            value,
                            str
                        ):
                            return clean_text(value)

                        return str(value)

    return ""


# ============================================================
# MAIN PARSER
# ============================================================

def parse_product(data, url=None):
    """
    Convert Blinkit network/API data into a Product object.

    The URL is used to identify the exact product.
    """

    product = Product()

    # --------------------------------------------------------
    # Get target product ID from URL
    # --------------------------------------------------------

    target_product_id = get_product_id_from_url(
        url
    )

    # --------------------------------------------------------
    # Product ID
    # --------------------------------------------------------

    product.product_id = find_product_id(
        data,
        target_product_id
    )

    # --------------------------------------------------------
    # Product information
    # --------------------------------------------------------

    product.title = find_title(
        data,
        product.product_id
    )

    product.brand = find_brand(
        data,
        product.product_id
    )

    product.description = find_description(
        data,
        product.product_id
    )

    product.category = find_category(
        data,
        product.product_id
    )

    product.price = find_price(
        data,
        product.product_id
    )

    product.weight = find_weight(
        data,
        product.product_id
    )

    # --------------------------------------------------------
    # PRODUCT IMAGES
    # --------------------------------------------------------

    product.images_url = find_images(
        data,
        product.product_id
    )

    # --------------------------------------------------------
    # INGREDIENTS
    # --------------------------------------------------------

    product.ingredients = find_ingredients(
        data,
        product.product_id
    )

    # --------------------------------------------------------
    # NUTRITION
    # --------------------------------------------------------

    product.nutritional_facts = (
        find_nutritional_facts(
            data,
            product.product_id
        )
    )

    return product


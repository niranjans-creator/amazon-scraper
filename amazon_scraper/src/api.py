
import requests
from config import ASIN_API_KEY, API_URL, AMAZON_DOMAIN


def get_product_data(asin):
    params = {
        "api_key": ASIN_API_KEY,
        "amazon_domain": AMAZON_DOMAIN,
        "asin": asin,
        "type": "product"
    }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()

    return response.json()
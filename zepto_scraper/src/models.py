from dataclasses import dataclass, field
from typing import List


@dataclass
class Product:
    title: str = ""
    description: str = ""
    weight: str = ""
    category: str = ""
    price: str = ""
    ingredients: str = ""
    image_urls: List[str] = field(default_factory=list)
    product_url: str = ""
from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):

    product_id: Optional[str] = None
    title: Optional[str] = None
    brand: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    weight: Optional[str] = None
    images_url: Optional[str] = None
    ingredients: Optional[str] = None
    nutritional_facts: Optional[str] = None
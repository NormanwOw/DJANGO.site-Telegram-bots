from typing import List

from pydantic import BaseModel

from main.domain.entities import Product


class Order(BaseModel):
    number: int
    phone_number: str
    user_id: int
    products: List[Product]
    total_price: int = 0

    @staticmethod
    def factory(
        number: int,
        phone_number: str,
        user_id: int,
        products: List[Product]
    ) -> 'Order':
        return Order(
            number=number,
            phone_number=phone_number,
            user_id=user_id,
            products=products,
            total_price=sum(product.price for product in products)
        )

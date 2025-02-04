import random
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, EmailStr

from main.domain.entities import Product


class Order(BaseModel):
    number: int
    phone_number: str
    email: EmailStr
    user_id: int
    products: List[Product]
    status: str = 'Оформлен'
    total_price: int = 0
    date: Optional[datetime] = Field(default_factory=datetime.utcnow)

    @staticmethod
    def factory(
        number: int,
        phone_number: str,
        email: str,
        user_id: int,
        products: List[Product]
    ) -> 'Order':
        return Order(
            number=number,
            phone_number=phone_number,
            email=email,
            user_id=user_id,
            products=products,
            total_price=sum(product.price for product in products)
        )

    @staticmethod
    def generate_order_number(order_numbers: list[int]) -> int:
        min_id = 10 ** 6
        max_id = 10 ** 7 - 1
        order_number = random.randint(min_id, max_id)

        while order_number in order_numbers:
            order_number += 1
            if order_number > max_id:
                order_number = random.randint(min_id, max_id)

        return order_number

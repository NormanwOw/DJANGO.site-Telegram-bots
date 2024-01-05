import random

from main.models import Order, Product


class UtilsOrder:

    @classmethod
    def get_order_number(cls) -> str:
        """Generate order number"""

        min_id = 10**6
        max_id = 10**7 - 1
        order_number = random.randint(min_id, max_id)
        order = Order.objects.filter(order_id=order_number)

        while len(order):
            order_number += 1
            if order_number > max_id:
                order_number = random.randint(min_id, max_id)
            order = Order.objects.filter(order_id=order_number)

        return str(order_number)

    @classmethod
    def get_order(cls, data: dict) -> dict:
        """Update order, set order number and total order price"""

        data['order_id'] = cls.get_order_number()
        data['bot_shop'] = True

        product_list = Product.objects.all()
        total_price = 0

        for item in product_list:
            if data[item.name]:
                total_price += item.price
                data[item.name] = item.price
            else:
                data[item.name] = 0

        data['total_price'] = total_price

        return data

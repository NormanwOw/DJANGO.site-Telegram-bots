from pydantic import BaseModel


class Product(BaseModel):
    id: int
    code: str
    name: str
    price: int
    title: str
    description: str

    @staticmethod
    def factory(
        _id: int,
        code: str,
        name: str = '',
        price: int = 0,
        title: str = '',
        description: str = '',
    ) -> 'Product':
        return Product(
            id=_id,
            code=code,
            name=name,
            price=price,
            title=title,
            description=description
        )

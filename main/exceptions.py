

class MainException(Exception):
    pass


class OrderException(MainException):
    pass


class OrderNotFoundException(OrderException):
    pass

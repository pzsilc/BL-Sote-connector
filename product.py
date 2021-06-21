class Product:
    def __init__(self, sku, quantity, to_skip, zero):
        self.__sku = sku
        self.__quantity = quantity
        self.__to_skip = to_skip
        self.__was_updated = False
        self.__zero = zero

    @property
    def sku(self):
        return self.__sku

    @property
    def quantity(self):
        return self.__quantity

    @property
    def to_skip(self):
        return self.__to_skip

    @property
    def zero(self):
        return self.__zero

    @property
    def was_updated(self):
        return self.__was_updated

    def updated(self):
        self.__was_updated = True
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

    def get_real_stock(self, set_0_if_less_than):
        if self.zero and self.quantity <= self.zero:
            return 0
        elif self.quantity <= set_0_if_less_than:
            return 0
        return self.quantity

    def get_sote_product(self, service, hash):
        try:
            return service.GetProductByCode({
                '_session_hash': hash,
                'code': self.sku
            })
        except:
            return None
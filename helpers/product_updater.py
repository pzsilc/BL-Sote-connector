class ProductUpdater:
    def __init__(self, api, _hash, set_0_if_less_than):
        self.api = api
        self.value0 = set_0_if_less_than
        self._hash = _hash

    def update(self, product):
        return self.api.service.UpdateProductByCode({
            '_session_hash': self._hash,
            'code': product.sku,
            'stock': product.get_real_stock(self.value0)
        })

    def update_option(self, product, sote_id):
        return self.api.service.UpdateProductOption({
            '_session_hash': self._hash,
            'option_id': sote_id,
            'stock': product.get_real_stock(self.value0)
        })

    def update_stock_validation(self, product):
        return self.api.service.UpdateProductByCode({
            '_session_hash': self._hash,
            'code': product.sku,
            'is_stock_validated': 1
        })
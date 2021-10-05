from handler import Handler
from product import Product
import requests
import json
import math


class Importer(Handler):
    def find_ignore_and_zero(self, features):
        ignore, zero = False, None
        for i in features:
            if i[0] == 'IGNORUJ':
                ignore = True
            if i[0] == 'ZERO':
                zero = int(i[1])
        return {
            'ignore': ignore,
            'zero': zero
        }


    def run(self):
        #get all products
        res = requests.post(self._auth['api'], data={
            'token': self._auth['token'],
            'method': 'getProductsList',
            'parameters': '{"storage_id": "bl_1"}'
        })
        res = res.text
        res = json.loads(res)
        if res['status'] == 'ERROR':
            print('Nie udało się połączyć z Baselinkerem. Sprawdź dostęp do internetu lub spróbuj za kilka minut\n')
            return
        products = res['products']

        #get details for products
        max_accept = 1000
        nb_of_requests = math.ceil(len(products) / max_accept)
        for stuff in range(nb_of_requests):
            ids = [i['product_id'] for i in products[ stuff * 1000 : (stuff + 1) * 1000]]
            ids = str(ids).replace("'", '')
            res = requests.post(self._auth['api'], data={
                'token': self._auth['token'],
                'method': 'getProductsData',
                'parameters': '{"storage_id": "bl_1", "products": ' + ids + '}'
            })
            res = json.loads(res.text)
            if res['status'] == 'ERROR':
                print('Nie udało się połączyć z Baselinkerem. Sprawdź dostęp do internetu lub spróbuj za kilka minut\n')
                return
            details = res['products']
            for key in details:
                obj = details[key]
                features = self.find_ignore_and_zero(obj['features'])
                to_skip = features['ignore']
                zero = features['zero']
                this_product = list(filter(lambda product: product['product_id'] == key, products))[0]
                this_product['to_skip'] = to_skip
                this_product['zero'] = zero
        #save products
        __products = list()
        for product in products:
            __products.append(Product(
                sku=product['sku'],
                quantity=product['quantity'],
                to_skip=product['to_skip'],
                zero=product['zero']
            ))
        return __products
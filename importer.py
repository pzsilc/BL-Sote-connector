from handler import Handler
from product import Product
import requests
import json
import math


class Importer(Handler):
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
                to_skip = True if len(obj['features']) > 0 and obj['features'][0][0] == 'IGNORUJ' else False
                zero = None
                if len(obj['features']) == 2 and obj['features'][1][0] == 'ZERO':
                    try:
                        zero = int(obj['features'][1][1])
                    except:
                        pass
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
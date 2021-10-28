from .handler import Handler
from helpers.product import Product
import requests, json, time

class Importer(Handler):
    storage_id = 'bl_1'
    max_accept = 1000
    page = 1
    IGNORE = 'ignoruj'
    ZERO = 'zero'

    def find_ignore_and_zero(self, features):
        ignore, zero = False, None
        for feature in features:
            if feature[0].lower() == Importer.IGNORE:
                ignore = True
            if feature[0].lower() == Importer.ZERO:
                zero = int(feature[1])
        return { 'ignore': ignore, 'zero': zero }

    def send_request(self, method, parameters):
        try:
            res = requests.post(self._auth['api'], data={
                'token': self._auth['token'],
                'method': method,
                'parameters': parameters
            })
            res = json.loads(res.text)
            if res['status'] == 'ERROR':
                print(res)
                raise Exception()
            return res['products']
        except Exception as e:
            print(e)
            print('\n\nNie udało się połączyć z Baselinkerem. Sprawdź dostęp do internetu lub spróbuj za kilka minut\n')
            exit(0)

    def get_products_page_by_page(self):
        while True:
            products = self.send_request("getProductsList", '{"storage_id": "' + self.storage_id + '", "page": ' + str(Importer.page) + '}')
            if len(products) == 0:
                break
            print(f"Pobrano stronę {Importer.page} produktów", "(", len(products), ")")
            time.sleep(5)
            Importer.page += 1
            yield products

    def run(self):
        all_products = []
        for products in self.get_products_page_by_page():
            ids_list = [product['product_id'] for product in products]
            ids_str = str(ids_list).replace("'", '')
            details = self.send_request("getProductsData", '{"storage_id": "' + self.storage_id + '}", "products": ' + ids_str + '}')
            for key in details:
                product_with_details = details[key]
                features = self.find_ignore_and_zero(product_with_details['features'])
                matched_products = list(filter(lambda product: product['product_id'] == key, products))
                if len(matched_products) == 0:
                    print('Baselinker nie zwrócił detali produktu')
                this_product = matched_products[0]
                this_product['to_skip'] = features['ignore']
                this_product['zero'] = features['zero']
            all_products += products
        return list(map(
            lambda product: Product(
                sku=product['sku'],
                quantity=product['quantity'],
                to_skip=product['to_skip'],
                zero=product['zero']
            ),
            all_products
        ))
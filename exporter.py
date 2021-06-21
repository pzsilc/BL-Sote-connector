from handler import Handler
from zeep import Client
import re
import json
from colorama import Fore, Style, init
init()



class Exporter(Handler):

    def filter_products_by_sku(self, products, sku):
        res = list(filter(lambda x: x.sku == sku, products))
        return res[0] if len(res) else None



    def write_logs(self, text, updated_increase=False, product=None):
        print(text)
        if updated_increase:
            self.updated += 1
        if self.logsfile:
            self.logsfile.write(text + '\n')
        if product:
            product.updated()
    


    def run(self, **kwargs):
        products = kwargs['products']
        set_0_if_less_than = kwargs['set_0_if_less_than']
        self.logsfile = kwargs['logsfile']
        self.updated = 0
        webapi = Client(self._auth['api_login'])
        _hash = webapi.service.doLogin({
            "username": self._auth['username'],
            "password": self._auth['password']
        })
        webapi = Client(self._auth['api'])
        pattern = re.compile('{(.*)}')

        for product in products:
            if product.to_skip:
                continue
            try:
                sote_product = webapi.service.GetProductByCode({
                    '_session_hash': _hash,
                    'code': product.sku
                })
            except:
                continue

            if sote_product['product_options'] and sote_product['product_options']!='{ "typ_ceny": "brutto" }' and sote_product['product_options']!='{ "typ_ceny": "netto" }':
                #produkt jest "wirtualny" (ma tylko opcje)
                arr = ['{'+i+'}' for i in pattern.findall(sote_product['product_options'])]
                arr = [json.loads(i) for i in arr if 'kod' in json.loads(i)]
                for i in arr:
                    filtered_product = self.filter_products_by_sku(products, i['kod'])
                    if filtered_product:
                        qty = filtered_product.quantity
                        if filtered_product.zero and filtered_product.quantity <= filtered_product.zero:
                            qty = 0
                        elif filtered_product.quantity <= set_0_if_less_than:
                            qty = 0
                        webapi.service.UpdateProductOption({
                            '_session_hash': _hash,
                            'option_id': i['id'],
                            'stock': qty
                        })
                        self.write_logs(
                            Fore.CYAN + f'Opcja ' + i['kod'] + f' produktu {product.sku} została zaktualizowana',
                            updated_increase=True,
                            product=filtered_product
                        )
                webapi.service.UpdateProductByCode({
                    '_session_hash': _hash,
                    'code': product.sku,
                    'is_stock_validated': 1
                })
            else:
                #produkt jest rzeczywisty (bez opcji, aktualizacja bezpośrednia)
                qty = product.quantity
                if product.zero and product.quantity <= product.zero:
                    qty = 0
                elif product.quantity <= set_0_if_less_than:
                    qty = 0
                webapi.service.UpdateProductByCode({
                    '_session_hash': _hash,
                    'code': product.sku,
                    'stock': qty
                })
                self.write_logs(
                    Fore.GREEN + f'Produkt {product.sku} został zaktualizowany', 
                    updated_increase=True,
                    product=product
                )
        for product in products:
            if not product.was_updated:
                self.write_logs(Fore.RED + f'Produkt {product.sku} nie został znaleziony')
        self.write_logs(Style.RESET_ALL + 'Koniec' + f'\nZaktualizowano {self.updated} produktów\n\n\n\n')
        return self
from .handler import Handler
from helpers.options_extractor import OptionsExtractor
from helpers.product_updater import ProductUpdater
from helpers.log import Log
from zeep import Client
from colorama import Fore, init
init()



class Exporter(Handler):
    def __init__(self, auth, products=[], set_0_if_less_than=0, logsfile=None):
        super(Exporter, self).__init__(auth)
        self.products = products
        self.set_0_if_less_than = set_0_if_less_than
        self.hash = None
        Log.set_logs_file(logsfile)

    def filter_products_by_sku(self, sku): #filtrowanie listy produktów po sku, używane podczas updatu 
        res = list(filter(lambda x: x.sku == sku, self.products))
        return res[0] if len(res) else None

    def login(self): #logowanei do soap sote
        webapi = Client(self._auth['api_login'])
        self.hash = webapi.service.doLogin({
            "username": self._auth['username'],
            "password": self._auth['password']
        })
        return bool(self.hash)
    
    def run(self):
        webapi = Client(self._auth['api'])
        if not self.login(): #jeśli nie udało się zalogować to zatrzymaj program
            print("Nie udało się zalogować do sote")
            exit(0)
        #tworzenie updateru
        updater = ProductUpdater(webapi, self.hash, self.set_0_if_less_than)
        #aktualizacja produktów pojedynczo
        for product in self.products: #aktualizacja produktów (główna pętla)
            sote_product = product.get_sote_product(webapi.service, self.hash) #pobieranie odpowiednika produktu w sote
            if not sote_product or product.to_skip: #jeśli nie ma lub produkt jest do pominięcia to pomija
                continue
            options = OptionsExtractor.extract(sote_product) #pobieranie opcji produktu z sote
            if len(options):
                for option in options: #produkt jest "wirtualny" (ma tylko opcje)
                    product_option = self.filter_products_by_sku(sku=option['kod'])
                    if product_option:
                        updater.update_option(product, option["id"])
                        Log(Fore.CYAN + f'Opcja ' + option['kod'] + f' produktu {product.sku} została zaktualizowana', True, product_option)
                updater.update_stock_validation(product) #aktalizacja stock_validation dla produktu bazowego opcji (sprawdza wtedy te ilości, musi być na True)
            else:
                updater.update(product) #produkt jest rzeczywisty (bez opcji, aktualizacja bezpośrednia)
                Log(Fore.GREEN + f'Produkt {product.sku} został zaktualizowany', True, product)
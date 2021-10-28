from datetime import date
from .exporter import Exporter
from .importer import Importer
from helpers.log import Log

class App:
    updated_nb = 0
    config = None
    logsfile = None
    importer = None
    exporter = None

    def __init__(self, config):
        self.config = config
        if App.updated_nb == config['logs_interval_days'] * len(config['hours']):
            App.updated_nb = 0
            today = date.today()
            self.logsfile = open(config['logspath'] + f'/{today.strftime("%b-%d-%Y")}.txt', 'w')
        App.updated_nb += 1

    def start(self):
        print("Pobieranie produktów z BaseLinkera...")
        self.importer = Importer(self.config['baselinker'])
        products = self.importer.run()
        print("Pobieranie zakończone", "(Pobrano", len(products), "produktów)")
        print("Eksport produktów do Sote")
        self.exporter = Exporter(
            auth=self.config['soteshop'], 
            products=products, 
            set_0_if_less_than=self.config['set_0_if_less_than'], 
            logsfile=self.logsfile)
        self.exporter.run()
        print("Eksport zakończony")

    def summary(self):
        not_updated_products = list(filter(lambda x: not x.was_updated, self.exporter.products))
        for index, product in enumerate(not_updated_products):
            print(str(index + 1) + ". Produkt: " + product.sku)
        nb = str(Log.updated)
        print(f"\nZaktualizowano {nb} produktów")
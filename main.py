import json
import time, schedule
from datetime import date
from exporter import Exporter
from importer import Importer
config = None
with open('config.txt') as config_file:
    config = json.loads(config_file.read())


class App:
    updated_nb = 0

    def __init__(self):
        self.logsfile = None
        if App.updated_nb == config['logs_interval_days'] * len(config['hours']):
            App.updated_nb = 0
            today = date.today()
            self.logsfile = open(config['logspath'] + f'/{today.strftime("%b-%d-%Y")}.txt', 'w')
        App.updated_nb += 1

    def __del__(self):
        if self.logsfile:
            self.logsfile.close()

#run to import danych z BL i natychmiastowy eksport ich do Sote'a
def run():
    app = App()
    products = Importer(config['baselinker']).run()
    Exporter(config['soteshop']).run(products=products, set_0_if_less_than=config['set_0_if_less_than'], logsfile=app.logsfile)
    del app

if __name__ == '__main__':
    #for hour in config['hours']:
    #    schedule.every().day.at(hour).do(run)
    #while True:
    #    schedule.run_pending()
    #    time.sleep(1)
    run()
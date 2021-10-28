from core.app import App
import json

config = None
with open('config.json') as config_file:
    config = json.loads(config_file.read())

def run():
    app = App(config)
    app.start()
    app.summary()

if __name__ == '__main__':
    run()

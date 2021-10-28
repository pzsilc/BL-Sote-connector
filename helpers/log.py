class Log:
    all_logs = []
    updated = 0
    logs_file = None

    def set_logs_file(file):
        Log.logs_file = file

    def __init__(self, text, increase_update=False, product=None):
        self.text = text
        self.increare_update = increase_update
        self.product = product
        self.print()
        self.actions()
        Log.all_logs.append(self)

    def print(self):
        print(self.text)

    def actions(self):
        if self.product:
            self.product.updated()
        if self.increare_update:
            Log.updated += 1
        if Log.logs_file:
            Log.logs_file.write(self.text + '\n')
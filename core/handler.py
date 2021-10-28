import abc

class Handler(metaclass=abc.ABCMeta):
    def __init__(self, auth):   
        self._auth = auth

    @abc.abstractmethod
    def run(self):
        pass
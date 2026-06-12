from abc import ABC, abstractmethod


class BaseParser(ABC):

    def __init__(self, company):
        self.company = company

    @abstractmethod
    def run(self):
        pass
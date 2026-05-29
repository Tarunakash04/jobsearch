from src.parsers.base_parser import BaseParser


class GreenhouseParser(BaseParser):

    def __init__(self, company):

        super().__init__(company)

    def run(self):

        print("[INFO] Greenhouse parser started")

        return []
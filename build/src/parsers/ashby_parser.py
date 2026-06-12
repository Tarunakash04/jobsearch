from src.parsers.base_parser import BaseParser


class AshbyParser(BaseParser):

    def __init__(self, company):

        super().__init__(company)

    def run(self):

        print("[INFO] Ashby parser started")

        return []
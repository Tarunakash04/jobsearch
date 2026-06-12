from src.parsers.base_parser import BaseParser


class LeverParser(BaseParser):

    def __init__(self, company):

        super().__init__(company)

    def run(self):

        print("[INFO] Lever parser started")

        return []
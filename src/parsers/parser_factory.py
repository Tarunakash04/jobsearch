from src.parsers.smartrecruiters_parser import SmartRecruitersParser
from src.parsers.workday_parser import WorkdayParser
from src.parsers.greenhouse_parser import GreenhouseParser
from src.parsers.lever_parser import LeverParser
from src.parsers.ashby_parser import AshbyParser


class ParserFactory:

    @staticmethod
    def get_parser(company):

        ats = company.get("ats", "").lower()

        mapping = {
            "smartrecruiters": SmartRecruitersParser,
            "workday": WorkdayParser,
            "greenhouse": GreenhouseParser,
            "lever": LeverParser,
            "ashby": AshbyParser
        }

        parser_class = mapping.get(ats)

        if not parser_class:
            raise Exception(f"Unsupported ATS: {ats}")

        return parser_class(company)
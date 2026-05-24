from src.parsers.gemini_parser import GeminiParser

url = "https://jobs.smartrecruiters.com/Freshworks/744000123362189-lead-software-engineer-site-reliability"

parser = GeminiParser()

result = parser.parse_job(url)

print("\n========== GEMINI OUTPUT ==========\n")
print(result)
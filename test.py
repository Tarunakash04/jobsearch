import requests
import time

url = "https://statestreet.wd1.myworkdayjobs.com/wday/cxs/statestreet/Global/jobs"

payload = {
    "appliedFacets": {},
    "limit": 20,
    "offset": 0,
    "searchText": ""
}

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://statestreet.wd1.myworkdayjobs.com/Global",
    "Origin": "https://statestreet.wd1.myworkdayjobs.com"
}

print("Starting request...")

start = time.time()

response = requests.post(
    url,
    json=payload,
    headers=headers,
    timeout=15
)

print(f"Time: {round(time.time()-start,2)}s")
print(f"Status: {response.status_code}")

print(response.text[:500])
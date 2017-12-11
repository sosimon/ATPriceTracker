import requests

BASEURL = "https://www.autotrader.com/rest/searchresults/base"

def get(filters):
  headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
  }
  resp = requests.get(BASEURL, params=filters, headers=headers)
  return resp

def lambda_handler(event, context):
  filters = {
    "makeCodeList": event.get("makeCodeList") if "makeCodeList" in event else "HONDA",
    "modelCodeList": event.get("modelCodeList") if "modelCodeList" in event else "S2000",
    "zip": event.get("zip") if "zip" in event else "95054",
    "searchRadius": event.get("searchRadius") if "searchRadius" in event else "500",
    "listingTypes": "used",
    "startYear": "1981",
    "numRecords": "100"
  }
  r = get(filters)
  return r.json()
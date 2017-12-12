import requests
import json
import boto3
import datetime

BASEURL = "https://www.autotrader.com/rest/searchresults/base"
SQSURL = "https://sqs.us-west-2.amazonaws.com/490069154287/autotrader-payloads"

# get search results from AT using search parameters specified in search_params
def get(search_params):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }
    resp = requests.get(BASEURL, params=search_params, headers=headers)
    return resp

def put_message(message):
    client = boto3.client('sqs')
    resp = client.send_message(
        QueueUrl=SQSURL,
        MessageBody=message
    )
    return resp

def filter_results(raw):
    listings = raw["listings"]
    output = []
    for l in listings:
        output.append({
            "listingId": l.get("listingId"),
            "makeCode": l.get("makeCode"),
            "modelCode": l.get("modelCode"),
            "firstPrice": l.get("firstPrice"),
            "derivedPrice": l.get("derivedPrice"),
            "salePrice": l.get("salePrice"),
            "colorExteriorSimple": l.get("colorExteriorSimple") if "colorExteriorSimple" in l else "",
            "maxMileage": l["maxMileage"],
            "title": l["title"],
            "retrieveDate": datetime.datetime.now()
        })
    return output

def lambda_handler(event, context):
    search_params = {
        "makeCodeList": event.get("makeCodeList") if "makeCodeList" in event else "HONDA",
        "modelCodeList": event.get("modelCodeList") if "modelCodeList" in event else "S2000",
        "zip": event.get("zip") if "zip" in event else "95054",
        "searchRadius": event.get("searchRadius") if "searchRadius" in event else "500",
        "listingTypes": "used",
        "startYear": "1981",
        "numRecords": "100"
    }
    r = get(search_params)
    message = filter_results(r.json())
    r1 = put_message(json.dumps(message))
    return r1

import json
import boto3
import psycopg2
import re
import datetime

SQSURL = "https://sqs.us-west-2.amazonaws.com/490069154287/autotrader-payloads"

client = boto3.client('sqs')

db_host = "autotrader.cuicpsblup3n.us-west-2.rds.amazonaws.com"
db_port = 5432
db_name = "autotrader"
db_user = "administrator"
db_pass = "secretpassword"
db_table = "price"

def get_message(client):
    return client.receive_message(QueueUrl=SQSURL)

def delete_message(client, receipt_handle):
    return client.delete_message(QueueUrl=SQSURL, ReceiptHandle=receipt_handle)

def process_records(message):
    print("Processing message: {}".format(message)) 
    conn = make_conn()
    for listing in json.loads(message):
        l = prep_data(listing)
        query = "INSERT INTO price (listingid, make, model, year, mileage, color, price, createdate) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(l.get("listing_id"), l.get("make"), l.get("model"), l.get("year"), l.get("mileage"), l.get("color"), l.get("price"), l.get("createdate"))
        exec_query(conn, query)
    conn.commit()
    conn.close()

def prep_data(listing):
    listing_id = listing.get("listingId")
    make = listing.get("makeCode")
    model = listing.get("modelCode")
    year = re.match(r".*\s(\d{4})\s.*", listing.get("title")).group(1)
    mileage = listing.get("maxMileage").split(" ")[0].replace(",", "")
    color = listing.get("colorExteriorSimple") if "colorExteriorSimple" in listing else "UNKNOWN"
    price = 0
    if listing.get("derivedPrice"):
        price = listing.get("derivedPrice")
    elif listing.get("salePrice"):
        price = listing.get("salePrice")
    elif listing.get("firstPrice"):
        price = listing.get("firstPrice")
    price = str(price).replace("$", "").replace(",", "")
    createdate = listing.get("retrieveDate")
    clean_listing = {
        "listing_id": listing_id,
        "make": make,
        "model": model,
        "year": year,
        "mileage": mileage,
        "color": color,
        "price": price,
        "createdate": createdate
    }
    return clean_listing

def make_conn():
    conn = None
    try:
        conn = psycopg2.connect("dbname='{}' user='{}' host='{}' password='{}'".format(db_name, db_user, db_host, db_pass))
    except:
        print("Unable to connect to the database {}".format(db_host))
    return conn

def exec_query(conn, query):
    print("Executing query: {}".format(query))
    cur = conn.cursor()
    cur.execute(query)

def lambda_handler(event, context):
    # get message from queue
    r = get_message(client)
    print(r)

    # check for empty message
    messages = r.get("Messages")
    message = None
    if messages:
        message = messages[0]
        print(message)
    else:
        print("No messages to process")
        return

    # get message receipt handle
    receipt_handle = message.get("ReceiptHandle")

    # process listings (write to database)
    process_records(message.get("Body"))

    # delete message from queue
    r1 = delete_message(client, receipt_handle)
    
    return r1

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
  resp = client.delete_message(
    QueueUrl=SQSURL,
    ReceiptHandle=receipt_handle
  )
  return resp

def process_records(message):
  print("Processing message: {}".format(message)) 
  conn = make_conn()
  for listing in message:
    listing_id = listing.get("listingId")
    make = "Honda"
    model = "S2000"
    year = re.match(r".*\s(\d{4})\s.*", listing.get("title")).group(1)
    mileage = listing.get("maxMileage")
    color = listing.get("colorExteriorSimple")
    price = listing.get("derivedPrice")
    createdate = datetime.datetime.now()
    query = "INSERT INTO price (listingid, make, model, year, mileage, color, price, createdate) VALUES ({}, {}, {}, {}, {}, {}, {}, {})".format(listing_id, make, model, year, mileage, color, price, createdate)
    exec_query(conn, query)
  conn.commit()
  conn.close()

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
  resp = get_message(client)
  print(resp)
  #messages = resp.get("Messages")
  #message = ""
  #if messages:
  #  message = messages[0]
  #  print(message)
  #else:
  #  print("No messages to process")
  #  return
  #receipt_handle = message.get("ReceiptHandle")
  #process_records(message.get("Body"))
  #r1 = delete_message(client, receipt_handle)

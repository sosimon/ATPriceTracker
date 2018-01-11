# app.py

from flask import Flask, g, render_template
import psycopg2
import requests

app = Flask(__name__)
app.config.from_object('config')

def connect_db():
    conn = None
    params = "dbname='{}' user='{}' host='{}' password='{}'".format(
            app.config["DB_NAME"],
            app.config["DB_USER"],
            app.config["DB_HOST"],
            app.config["DB_PASS"])
    try:
        conn = psycopg2.connect(params)
        print("INFO: Connected to database!")
    except:
        print("ERROR: Could not connect to the database!")
    return conn

def get_db_conn():
    if not hasattr(g, "pg_db"):
        g.pg_db = connect_db()
    return g.pg_db

def get_metadata(path):
    META_URL = "http://metadata.google.internal/computeMetadata/v1/"
    headers = {"Metadata-Flavor": "Google"}
    url = META_URL + path
    r = ""
    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(e)
    return r

@app.teardown_appcontext
def close_db(exception):
    if hasattr(g, 'pg_db'):
        g.pg_db.close()

@app.route("/")
def index():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT listingId, mileage, price FROM price WHERE price != 0;")
    data = cur.fetchall()
    print("INFO: {} rows fetched".format(cur.rowcount))
    cur.close()
    return render_template("index.html", data=data)

@app.route("/healthz")
def healthz():
    instance = {}
    instance["name"] = get_metadata("instance/name")
    instance["hostname"] = get_metadata("instance/hostname")
    instance["id"] = get_metadata("instance/id")
    instance["zone"] = get_metadata("instance/zone")
    instance["internalip"] = get_metadata("instance/network-interfaces/0/ip")
    instance["externalip"] = get_metadata("instance/network-interfaces/0/forwarded-ips")
    instance["project"] = get_metadata("project/project-id")
    return render_template("healthz.html", instance=instance)

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True, port=80)

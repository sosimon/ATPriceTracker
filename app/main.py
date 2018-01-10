# app.py

from flask import Flask, g, render_template
import psycopg2

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

@app.teardown_appcontext
def close_db(exception):
    if hasattr(g, 'pg_db'):
        g.pg_db.close()

@app.route("/")
def main():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT listingId, mileage, price FROM price WHERE price != 0;")
    data = cur.fetchall()
    print("INFO: {} rows fetched".format(cur.rowcount))
    cur.close()
    return render_template("index.html", data=data)

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True, port=80)

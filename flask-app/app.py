from flask import Flask, render_template, request, flash, redirect
import json
import datetime
import requests as r
from amadeus_rest import make_request
from flask_sqlalchemy import SQLAlchemy
from distance import haversine
import psycopg2 as pg
import psycopg2.extras

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://king-ict:king-ict@localhost/king-ict"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "top-secret"


db = SQLAlchemy(app)

airport = db.Table('airports', db.metadata, autoload=True, autoload_with=db.engine)

@app.route("/", methods=["GET"])
def pocetna():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    data = request.form
    data = dict(data)
    data['src_iata'] = data['src_iata'].upper()
    data['dest_iata'] = data['dest_iata'].upper()

    for key in data:
        if data[key] is None or len(data[key]) == 0:
            flash(f"You must enter {key}!")
            return redirect("/")

    try:
        if datetime.date.fromisoformat(data['dd']) < datetime.date.today():
            flash("Departure cannot be before today.")
            return redirect("/")
        if datetime.date.fromisoformat(data['rd']) < datetime.date.fromisoformat(data['dd']):
            flash("Return date cannot be before departure date.")
            return redirect("/")
    except Exception as e:
        return f"{e}", 400
    if len(data['src_iata']) != 3 or len(data['dest_iata']) != 3:
        return "IATA is a 3 letter code!", 400

    src_iata = db.session().query(airport).filter_by(IATA=data['src_iata']).first()

    dest_iata = db.session().query(airport).filter_by(IATA=data['dest_iata']).first()

    air_distance_km = haversine(src_iata.lng, src_iata.lat, dest_iata.lng, dest_iata.lat)

    msg = f"Distance between {src_iata.Airport_name } and {dest_iata.Airport_name} is {air_distance_km} km."

    conn = pg.connect("dbname='king-ict' user='king-ict' password='king-ict' host='localhost'")
    cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cur.execute(f"""SELECT * FROM flights WHERE "src_iata" = '{data['src_iata']}' AND "dest_iata" = '{data['dest_iata']}' and DATE("departureDate") = '{data['dd']}' and DATE("returnDate") = '{data['rd']}' and "currency" = '{data['currency']}' and "numOfAdults" = {data['numOfAdults']}""")
    flights = cur.fetchall()

    if len(flights) == 0:
        res = make_request(data['src_iata'], data['dest_iata'], data['dd'], data['rd'], data['numOfAdults'], data['currency'])
        if res[0] != 200:
            return f"Amadeus API doesn't work {res.status_code}", 500
        else:
            res_data = res[1]
            res_data = res_data['amadeus_data']
            if len(res_data) == 0:
                flash("no flights found!")
                return render_template("index.html")
            for row in res_data:
                print("executing insert")

                try:
                    cur.execute("""INSERT INTO flights ("src_iata", "dest_iata", "departureDate", "departureNumOfTransfers", "duration", "returnDate", "returnNumOfTransfers", "lastTicketingDate", "numOfavSeats", "numOfAdults", "currency", "total") VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )""", [ row['src_iata'], row['dest_iata'], row['departureDate'], row['departureNumOfTransfers'], row['duration'], row['returnDate'], row['returnNumOfTransfers'], row['lastTicketingDate'], row['numOfavSeats'], row['numOfAdults'], row['currency'], row['total'] ] )
                    conn.commit()
                except Exception as e:
                    print(e)
                    return f"{e}", 500
            cur.close()
            return render_template("table.html", data=res_data, dist_msg=msg)
    else:
        print("imam podatke!")
        tmp = dict()
        tmp['amadeus_data'] = flights
        flash("using cached results!")
        return render_template("table.html", data=flights, dist_msg=msg)
    
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=9090)

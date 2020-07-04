import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Creating Engine

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#Reflecting An Existing DB in a New Model

base = automap_base()

# Reflecting Tables
base.prepare(engine, reflect=True)

# Save References to Tables
measurement = base.classes.measurement
station = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine) 

# Setting Up Flask
app = Flask(__name__)

# Flask Routes 
@app.route("/")
def welcome():
    print("Listing all routes available..")
    return(
        f"Available Routes:<br/>"
        f"Availabile Routes: <br>"
        f"/api/v1.0/precipitation <br>"
        f"/api/v1.0/stations <br>"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>

    )

@app.route("/api/v1.0/precipitation")
def prcp():

    lastdate = session.query(measurement.date).order_by(measurement.date.desc()).first()
    oneyear = dt.date(2017,8,23) - dt.timedelta(days = 365)
    oneyearquery = session.query(measurement.date,measurement.prcp).filter(measurement.date >= oneyear).all()
    prcp = dict(oneyearquery)
    session.close()
    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():

    stationsquery = session.query(func.count(station.station)).all()
    stationresults = list(stationsquery)
    session.close()
    return jsonify(stationresults)

@app.route("/api/v1.0/tobs")
def tobs():

    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    max_date = max_date[0]
    year = dt.datetime.strptime(max_date, "%Y-%m-%d") - dt.timedelta(days=366)
    temp_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year).all()
    temp_list = list(np.ravel(temp_results))
    session.close()
    return jsonify(temp_list)

if __name__ == '__main__':
    app.run(debug=True)




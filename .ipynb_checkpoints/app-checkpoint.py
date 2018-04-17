import sqlalchemy
import pandas as pd
import numpy as np
import matplotlib
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
import datetime as dt
import matplotlib.pyplot as plt
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect = True)

Station = Base.classes.station
Measurements = Base.classes.measurements

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"for the following, enter your start date as YYYY-MM-DD for start and or end<br/>"
        f"<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    rain_dates = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date>last_year).order_by(Measurements.date).all()
    
    total_rain = []
    
    for rain in rain_dates:
        row = {}
        row["date"]=rain_dates[0]
        row["prcp"]=rain_dates[1]
        total_rain.append(row)
    
    return jsonify(total_rain)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station,Station.name).all()
    stations_names = []
    
    for station in stations:
        row = {}
        row["station"] = station[0]
        row["name"] = station[1]
        stations_names.append(row)
        
        
    return jsonify(stations_names)


@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperature = session.query(Measurements.date, Measurements.tobs).filter(Measurements.date>=last_year).order_by(Measurements.date).all()
    
    temp_total = []
    
    for temp in temperature:
        row = {}
        row["date"] = temperature[0]
        row["tobs"] = temperature[1]
        temp_total.append(row)
    
    return jsonify(temp_total)


@app.route("/api/v1.0/<start>")
def starting(start):   
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    trip_data = session.query(func.min(Measurements.tobs), func.max(Measurements.tobs), func.avg(Measurements.tobs)).filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):   
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    trip_data = session.query(func.min(Measurements.tobs), func.max(Measurements.tobs),func.avg(Measurements.tobs)).filter(Measurements.date >= start).filter(Measurements.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)
    
    


if __name__ == "__main__":
    app.run(debug=True)
    



# Assignment 10 Step 2
# Import 
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime 
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Home page route
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# Precipitation Page route
@app.route("/api/v1.0/precipitation")
def preciptiation():
    results = session.query(Measurement).all()

    precipitation = []
    for i in results:
        weather = {}
        weather[i.date] = i.prcp
        precipitation.append(weather)
    
    return jsonify(precipitation)


# List of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    
    results = session.query(Station.name).all()

    station_names = list(np.ravel(results))
    print(len(station_names))

    return jsonify(station_names)


# Query for the dates and temperature observation from a year the last data point
@app.route("/api/v1.0/tobs")
def tobs():
    recent_date, = session.query(Measurement.date).\
    order_by(Measurement.date.desc()).first()

    recent_date = datetime.strptime(recent_date, '%Y-%m-%d')

    year_ago = recent_date - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > year_ago).\
        order_by(Measurement.date).all()

    previous_year_temp = list(np.ravel(results))
    print(len(previous_year_temp))

    return jsonify(previous_year_temp)



# Query for Min temperature, the average temperature, and the max temperature given store os start-end range.
@app.route("/api/v1.0/<start>")
def weather(start):
    
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs),func.max(Measurement.tobs)]

    return jsonify(session.query(*sel).filter(func.strftime("%y-%m-%d", Measurement.date) == start).all())


# Define main behavior
if __name__ == "__main__":
    app.run(debug=True)



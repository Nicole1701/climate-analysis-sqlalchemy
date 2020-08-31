# Import
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the tables
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"<br/>"
        f"Available Routes: <br/><br/>"
        f"<a href='/api/v1.0/precipitation'>Precipitation: /api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>Stations: /api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>Temperature Observed (TOBS): /api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/yyyy-mm-dd'>Temp Stats by Start Date: /api/v1.0/yyyy-mm-dd</a><br/>"
        f"<a href='/api/v1.0/yyyy-mm-dd/yyyy-mm-dd'>Temp Stats by Start/End Date: /api/v1.0/yyyy-mm-dd/yyyy-mm-dd</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
  # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all countries' invoice totals
    results = session.query(measurement.date, measurement.prcp).order_by(measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_results
    precip_results = []

    for date, prcp in results:
        item_dict = {}
        item_dict["Date"] = date
        item_dict["Precipitation"] = prcp
        precip_results.append(item_dict)

    return jsonify(precip_results)

if __name__ == '__main__':
    app.run(debug=True)
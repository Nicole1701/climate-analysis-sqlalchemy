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

############ Home ############
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to my weather API!<br/>"
        f"Available Routes: <br/><br/>"
        f"Precipitation amounts by date: /api/v1.0/precipitation<br/>"
        f"List of stations: /api/v1.0/stations<br/>"
        f"Temperature Observed (TOBS) for most active station (last year only): /api/v1.0/tobs<br/>"
        f"Temp Stats by Start Date (YYYY-MM-DD): /api/v1.0/yyyy-mm-dd<br/>"
        f"Temp Stats by Start/End Date (YYYY-MM-DD): /api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
    )

############ Precipitation ############
@app.route("/api/v1.0/precipitation")
def precipitation():
  """Convert the query results to a dictionary using `date` as the key and `prcp` as the value.."""
  session = Session(engine)
  results = session.query(measurement.date, measurement.prcp).order_by(measurement.date).all()

  session.close()

  # Create a dictionary and append to a list of results
  precip_results = []

  for date, prcp in results:
      item_dict = {}
      item_dict["date"] = date
      item_dict["precipitation"] = prcp
      precip_results.append(item_dict)

  return jsonify(precip_results)

############ Stations ############
@app.route("/api/v1.0/stations")
def stations():
  """Return a JSON list of stations from the dataset."""
  session = Session(engine)
  results = session.query(station.station).all()

  session.close()

  return jsonify(results)

############ TOBS ############
@app.route("/api/v1.0/tobs")
def tobs():
  """Query the dates and temperature observations of the most active station for the last year of data."""
  """Return a JSON list of temperature observations (TOBS) for the previous year."""
  session = Session(engine)

  # Query the most active station for the last year
  top_station = session.query(measurement.station).\
                group_by(measurement.station).\
                order_by(func.count(measurement.prcp).desc()).first()

  last_day = session.query(measurement.date).order_by(measurement.date.desc()).first()
  query_year = (dt.datetime.strptime(last_day[0],'%Y-%m-%d') - dt.timedelta(days=365)).strftime('%Y-%m-%d')

  results = session.query(measurement.date, measurement.tobs).\
    filter(measurement.station == top_station[0]).\
    filter(measurement.date >= query_year).all()

  session.close()

  # Create a dictionary and append to a list of results
  tobs_results = []

  for date, tobs in results:
      item_dict = {}
      item_dict["date"] = date
      item_dict["tobs"] = tobs
      tobs_results.append(item_dict)

  return jsonify(tobs_results)

############ START ############
@app.route("/api/v1.0/<start>")

def start_date(start):
  """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date."""
  
  session = Session(engine)
  results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).all()

  session.close()

  # Create a dictionary and append to a list of results
  start_results = []

  for min, avg, max in results:
      item_dict = {}
      item_dict["min"] = min
      item_dict["average"] = avg
      item_dict["max"] = max
      start_results.append(item_dict)

  return jsonify(start_results)

############ START/END ############
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
  """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start and end date."""
  
  session = Session(engine)
  results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).filter(measurement.date <= end).all()

  session.close()

  # Create a dictionary and append to a list of results
  end_results = []

  for min, avg, max in results:
      item_dict = {}
      item_dict["min"] = min
      item_dict["average"] = avg
      item_dict["max"] = max
      end_results.append(item_dict)

  return jsonify(end_results)

if __name__ == '__main__':
    app.run(debug=True)
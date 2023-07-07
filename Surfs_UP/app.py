# Import the dependencies.
import numpy as np

import sqlalchemy
import json
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify 


#################################################
# Database Setup
#################################################

#create engine and the engine connects to a file
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()


# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table

# Map the Measurment Class 
measurement = Base.classes.measurement



# Map the station Class.  USed capital S for Station because
#later on we refer to station column and they cannot be the same
Station = Base.classes.station

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

#HomePage with all routes
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"The dates in the following links can be altered in the web address.<br/>"
        f"The start or end date cannot be any later than 2017-08-23 and must be in the"
        f"YYYY-MM-DD format<br/><br/>"
        f"/api/v1.0/2016-08-23<br/>"
        f"/api/v1.0/2016-08-23/2017-08-23<br/>")
        

#going to extract precipitation from the database for the last 12 months
@app.route("/api/v1.0/precipitation")
def precipitation():
    #create session and link to Python database
    session = Session(engine)

    #Return precipitation for the ast 12 months.  We know from the previous
    # notes our dates for measurement will be from 2016-08-23 to 2017-08-23
        
    prec_results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= '2016-08-23').\
        order_by(measurement.date).all()
    
    #close Session
    session.close()
    
    #append the into to a dictionary
    prec_year = []
    for date, prcp in prec_results:
       prec_dict={}
       prec_dict["date"] = date
       prec_dict["prcp"] = prcp
       prec_year.append(prec_dict)
    #jasonified
    return jsonify(prec_year)

#return a JSON list of stations from the above dataset
@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    """Return a list of stations from the database""" 
    station_results = session.query(Station.station, Station.id).all()

    session.close()
   

    #append into a dictionary 
    stations_all = []
    for station, id in station_results:
        stations_all_dict = {}
        stations_all_dict['station'] = station
        stations_all_dict['id'] = id
        stations_all.append(stations_all_dict)

    #Jsonify the dictionary
    return jsonify (stations_all)

@app.route("/api/v1.0/tobs")
def tobs():

    #create session and link to Python database
    session = Session(engine)

    most_active_station_number = "USC00519281"

    #Query the dates and temperature observations of the most active
    #station from the previous l year of data.
    #last 12 months of data (2016-08-18 to 2017-08-18) from climate_starter

    tobs_results = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == most_active_station_number).\
        filter(measurement.date >= '2016-08-18').\
        order_by(measurement.date).all()
    
    session.close()

    #append to dictionary
    tobs_all = []
    for date,tobs in tobs_results:
        tobs_all_dict = {}
        tobs_all_dict['date'] = date
        tobs_all_dict['tobs'] = tobs
        tobs_all.append(tobs_all_dict)

    #Jsonify the dictionary
    return jsonify (tobs_all)

#need to make a function to set a start date 
@app.route("/api/v1.0/<start>")
def start_date(start):

    session = Session(engine)

    #change the date from string to datetime
    query_start = dt.datetime.strptime(start, '%Y-%m-%d').date()
    
    #make a list for the min,max & avg tobs depending on start date
    #entered

    start_date_results = [func.min(measurement.tobs),
                        func.max(measurement.tobs),
                        func.avg(measurement.tobs)]
    
    #filter the dates from the start date
    start_results = session.query(*start_date_results).\
        filter(func.strftime('%Y-%m-%d', measurement.date) >=query_start).all()
  
    session.close()

    #we know that the last date in the data set is 2017-08-23
    return (f"Temperature from {start} to 2017-08-23 (last recorded date):<br/>"
            f"Minimum temperature: {round(start_results[0][0], 1)} °F<br/>"
            f"Maximum temperature: {round(start_results[0][1], 1)} °F<br/>"
            f"Average temperature: {round(start_results[0][2], 1)} °F")
                
 #need to make a function to set a start end date 
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):

    session = Session(engine)

    #change the date from string to datetime
    query_Start = dt.datetime.strptime(start, '%Y-%m-%d').date()
    query_End = dt.datetime.strptime(end, '%Y-%m-%d').date()

    #make a list for the min,max & avg tobs depending on start date
    #entered

    start_end_date_results = [func.min(measurement.tobs),
                            func.max(measurement.tobs),
                            func.avg(measurement.tobs)]        
            
            
    #filter the dates from the start date
    start_end_results = session.query(*start_end_date_results).\
        filter(func.strftime('%Y-%m-%d', measurement.date) >=query_Start).\
        filter(func.strftime('%Y-%m-%d', measurement.date) <=query_End).all()
    
    session.close()
  
    #we know that the last date in the data set is 2017-08-23
    return (f"Temperature from {start} to {end}:<br/>"
            f"Minimum temperature: {round(start_end_results[0][0], 1)} °F<br/>"
            f"Maximum temperature: {round(start_end_results[0][1], 1)} °F<br/>"
            f"Average temperature: {round(start_end_results[0][2], 1)} °F")
 
    
    session.close()
if __name__ == '__main__':
    app.run(debug=True)

#After doing this section I feel as though I should be drinking when
#working with Flask




#import flask dependency
import numpy as np
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#create sql engine to connect to
engine = create_engine("sqlite:///hawaii.sqlite")

#creates a reflection for tables
Base = automap_base()
Base.prepare(engine, reflect=True)

Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station



app = Flask(__name__)

@app.route("/")
def welcome():
    print("Welcome to my weather API!")
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route('/api/v1.0/precipitation')
def precip():
    print('Precipitation Page')

    session = Session(engine)

    prcp_q = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    #data to append data into a JSON format
    all_prcp = []

    for date, prcp in prcp_q:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route('/api/v1.0/stations')
def stations():
    print('Stations')

    session = Session(engine)

    s = session.query(Station.station,Station.name).all()
    
    session.close()

    #data to append data into a JSON format
    station_list = []
    
    for station, name in s:

        station_dict = {}
        station_dict['station'] = station
        station_dict['name'] = name

        station_list.append(station_dict)
    
    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs_data():
    print('Temperature Data')

    session = Session(engine)

    temp = session.query(Measurement.station, Measurement.tobs, Station.id, Station.name)\
        .filter(Measurement.station==Station.station)\
            .filter(Measurement.date.between('2016-08-23','2017-08-23')).all()

    session.close()

    #data to append data into a JSON format
    tobs_list = []

    for station, tobs, id, name in temp:

        tobs_dict = {}
        tobs_dict['station'] = station
        tobs_dict['tobs'] = tobs
        tobs_dict['id'] = id
        tobs_dict['name'] = name

        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

if __name__=="__main__":
    app.run(debug=True)
    
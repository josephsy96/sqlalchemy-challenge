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


#Create a Flask application
app = Flask(__name__)


#Assign routes for the Flask API
@app.route("/")
def welcome():
    print("Welcome to my weather API!")
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>For example: /api/v1.0/2016-01-01<br/>"
        f"/api/v1.0/<start>/<end><br/>For example: /api/v1.0/2016-01-01/2017-01-01"
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

@app.route('/api/v1.0/<start>')
def start_date(start):

    session = Session(engine)

    #start_session = ct = session.query(func.min(Measurement.tobs).label('Min Temp'), func.avg(Measurement.tobs).label('Average Temp'),\
        #func.max(Measurement.tobs).label('Max Temp')).filter(Measurement.date >= str_iterator).all()
    start_session = ct = session.query(func.min(Measurement.tobs).label('Min Temp'), func.avg(Measurement.tobs).label('Average Temp'),\
        func.max(Measurement.tobs).label('Max Temp')).filter(Measurement.date >= start).all()
    
    session.close()

    #data to append data into a JSON format
    start_list = []

    for min_temp, avg_temp, max_temp in start_session:
        start_dict = {}
        start_dict['Min Temp'] = min_temp
        start_dict['Average Temp'] = avg_temp
        start_dict['Max Temp'] = max_temp

        start_list.append(start_dict)

    return jsonify(start_list)

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):

    session = Session(engine)

    s_e = session.query(func.min(Measurement.tobs).label('Min Temp'), func.avg(Measurement.tobs).label('Average Temp'),\
        func.max(Measurement.tobs).label('Max Temp')).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    session.close()

    se_list = []

    for min_temp, avg_temp, max_temp in s_e:
        se_dict = {}
        se_dict['Min Temp'] = min_temp
        se_dict['Average Temp'] = avg_temp
        se_dict['Max Temp'] = max_temp
        se_list.append(se_dict)

    return jsonify(se_list)
    

if __name__=="__main__":
    app.run(debug=True)
    
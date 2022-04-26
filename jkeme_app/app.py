# Used WK 10 - Day 3 - Activity 10 - Flask_With_ORM
import numpy as np
import pandas as pd
from flask import Flask, jsonify
from sqlalchemy import create_engine

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Database
# Week 10, Day 3, Activity 10 - Flask_with_ORM
path = "sqlite:///Resources/hawaii.sqlite"
engine = create_engine(path)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"""
        <ul>
            <li><a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a></li>
            <li><a href='/api/v1.0/stations'>//api/v1.0/stations</a></li>
            <li><a href='/api/v1.0/tobs'>///api/v1.0/tobs</a></li>
            <li><a href='/api/v1.0/2016-11-20'>/api/v1.0/2016-11-20</a></li>            
             <li><a href='/api/v1.0/2017-08-16/2017-08-31'>/api/v1.0/2017-08-16/2017-08-31</a></li>
        </ul
        """
    )

@app.route("/api/v1.0/precipitation")
def getPrcp():
    conn = engine.connect()
    query1 = """
        SELECT
            date,
            station,
            prcp
        FROM
            measurement
        ORDER BY
            date asc,
            station asc
        """

    precipitation_df = pd.read_sql(query1, conn)
    conn.close()
    data = precipitation_df.to_dict(orient="records")
    return(jsonify(data))

@app.route("/api/v1.0/stations")
def getStation():
    conn = engine.connect()
    query2 = """
            SELECT
                station,
                name
            FROM
                station;
            """
    station_df = pd.read_sql(query2, conn)
    conn.close()
    data2 = station_df.to_dict(orient="records")
    return(jsonify(data2))

@app.route("/api/v1.0/tobs")
def getTobs():
    conn = engine.connect()
    query3 = """
        SELECT
            station,
            date,
            tobs

        FROM
            measurement
        WHERE
            date >= '2016-08-23'
        AND
            station = 'USC00519281'
        ORDER BY
            date asc;
        """
    tobs_df = pd.read_sql(query3, conn)
    conn.close()
    data3 = tobs_df.to_dict(orient="records")
    return(jsonify(data3))

@app.route("/api/v1.0/<start>")
def getStart(start):
    conn = engine.connect()
    query4 = f"""
        SELECT
            min(tobs) as TMIN,
            avg(tobs) as TAVG,
            max(tobs) as TMAX
        FROM
            measurement
        WHERE
            date >= '{start}'
        """
    start_df = pd.read_sql(query4, conn)
    conn.close()
    data4 = start_df.to_dict(orient="records")
    return(jsonify(data4))

@app.route("/api/v1.0/<start>/<end>")
def getTempRanges(start, end):
    conn = engine.connect()
    query5 = f"""
        SELECT
            min(tobs) as TMIN,
            avg(tobs) as TAVG,
            max(tobs) as TMAX
        FROM
            measurement
        WHERE
            date >= '{start}'
        AND 
            date <= '{end}'
        """
    start_end_df = pd.read_sql(query5, conn)
    conn.close()
    data5 = start_end_df.to_dict(orient="records")
    return(jsonify(data5))

if __name__ == '__main__':
    app.run(debug=True)

#################################################
# Dependencies
#################################################
import numpy as np

from flask import Flask, render_template, jsonify, redirect
from flask_cors import CORS

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base #classes into tables
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, func, inspect, Column, Integer, String

import psycopg2
import os

from data.databaseEngineering import write_databases
from processing.makeGeojson import choropleth_geojson, shootings_geoJSON

#################################################
# Write Databases
# Do only first time when setting up herokuapp, otherwise, leave commented out
#################################################
# write_databases()

#################################################
# Engine Setup
#################################################
engine = create_engine(os.environ.get('DATABASE_URL', '') or 'postgres://lqehqdnexeuwdi:e299f2b76843b838b81976e7cb183859f28b1cd99e6aa417fdce1340ce00fece@ec2-54-243-210-70.compute-1.amazonaws.com:5432/dbenqc5p6hbe3e')
# engine = create_engine('sqlite:///data/data.sqlite', convert_unicode=True, echo=False)
# engine = create_engine('postgresql://nupur_mathur:1BPdfWvnTSvMGDrPp48u5pQF0@localhost/crime_data')

#################################################
# Save reference to each table in database
#################################################
Base = declarative_base()
Base.metadata.reflect(engine)

# State Data
class Vcr(Base):
    __table__ = Base.metadata.tables['vcr']

class Violent_Crime(Base):
    __table__ = Base.metadata.tables['violent_crime']

class Unemployment(Base):
    __table__ = Base.metadata.tables['unemployment']

class Population(Base):
    __table__ = Base.metadata.tables['population']

class Murder(Base):
    __table__ = Base.metadata.tables['murder']

class Median_Household_Income_Stderr(Base):
    __table__ = Base.metadata.tables['median_household_income_stderr']

class Median_Household_Income(Base):
    __table__ = Base.metadata.tables['median_household_income']

# State outline
class State_Coordinates(Base):
    __table__ = Base.metadata.tables['state_coordinates']

# Point Data
class School_Shootings(Base):
    __table__ = Base.metadata.tables['school_shootings']

# Annual Data
class Snap(Base):
    __table__ = Base.metadata.tables['snap']

class Foreclosure(Base):
    __table__ = Base.metadata.tables['foreclosure']

#################################################
# Session Setup
#################################################
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
CORS(app)

# Full dashboard
@app.route('/')
def index():
    """Return the dashboard homepage."""

    return render_template('index.html')

@app.route('/gauges_tweets')
def gauges_tweets():
    """Return the gauges/tweets page"""

    return render_template('gauges_tweets.html')

@app.route('/api/v1.0/crime/<year>')
def crime(year):

    # Select columns for output
    sel = [
            Vcr.state,
            State_Coordinates.coordType,
            State_Coordinates.coordinates
        ]

    # All tables to iterate through
    tables = [[Vcr.__table__.columns, Vcr],
              [Violent_Crime.__table__.columns, Violent_Crime],
              [Unemployment.__table__.columns, Unemployment],
              [Population.__table__.columns, Population],
              [Murder.__table__.columns, Murder],
              [Median_Household_Income_Stderr.__table__.columns, Median_Household_Income_Stderr],
              [Median_Household_Income.__table__.columns, Median_Household_Income]
    ]

    for i in tables:
        # Iterate through all table columns
        for c in i[0]:
            # If table column is the same as the year inputted
            if c == getattr(i[1],year):
                # Append it to the selection
                sel.append(c)

    # # Iterate through all table columns
    # for c in Vcr.__table__.columns:
    #     # If table column is the same as the year inputted
    #     if c == getattr(Vcr,year):
    #         # Append it to the selection
    #         sel.append(c)

    # # Query Selection for results (join two tables)
    # results = session.query(*sel).\
    #     join(State_Coordinates, State_Coordinates.stateId==Vcr.stateId).all()

    results = session.query(*sel).\
        join(State_Coordinates, State_Coordinates.stateId==Vcr.stateId).\
        join(Violent_Crime, Violent_Crime.stateId==Vcr.stateId).\
        join(Unemployment, Unemployment.stateId==Vcr.stateId).\
        join(Population, Population.stateId==Vcr.stateId).\
        join(Murder, Murder.stateId==Vcr.stateId).\
        join(Median_Household_Income, Median_Household_Income.stateId==Vcr.stateId).\
        join(Median_Household_Income_Stderr, Median_Household_Income_Stderr.stateId==Vcr.stateId).all()

    # Create geoJson
    geoJson = choropleth_geojson(results, year)

    return jsonify(geoJson)


@app.route('/api/v1.0/schoolShootings/<year>')
def schoolShootings(year):

    results = session.query(School_Shootings).filter_by(Year=year).all()

    # run function on results:
    geoJson = shootings_geoJSON(results)

    return jsonify(geoJson)


if __name__ == '__main__':
    app.run(debug=True)

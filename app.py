#################################################
# Dependencies
#################################################
import numpy as np

from flask import Flask, render_template, jsonify, redirect

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base #classes into tables
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, func, inspect, Column, Integer, String

import psycopg2
import os

from processing.makeGeojson import choropleth_geojson, shootings_geoJSON


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

class Ucr(Base):
    __table__ = Base.metadata.tables['ucr']

class State_Coordinates(Base):
    __table__ = Base.metadata.tables['state_coordinates']

class School_Shootings(Base):
    __table__ = Base.metadata.tables['school_shootings']

#################################################
# Session Setup
#################################################
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or 'postgres://lqehqdnexeuwdi:e299f2b76843b838b81976e7cb183859f28b1cd99e6aa417fdce1340ce00fece@ec2-54-243-210-70.compute-1.amazonaws.com:5432/dbenqc5p6hbe3e'

# Full dashboard
@app.route('/')
def index():
    """Return the dashboard homepage."""

    return render_template('index.html')

@app.route('/api/v1.0/crimeRate/<year>')
def crimeRate(year):
    y = 'y' + year

    sel = [
            Ucr.state,
            State_Coordinates.coordType,
            State_Coordinates.coordinates
      ]

    for c in Ucr.__table__.columns:
        if c == getattr(Ucr,y):
            sel.append(c)

    results = session.query(*sel).\
        join(State_Coordinates, State_Coordinates.stateId==Ucr.stateId).all()

    geoJson = choropleth_geojson(results, year)

    return jsonify(geoJson)


@app.route('/api/v1.0/schoolShootings/<year>')
def schoolShootings(year):

    results = session.query(School_Shootings).filter_by(Year=year).all()

    # run function on results:
    geoJson = shootings_geojson(results)

    return jsonify(geoJson)


if __name__ == '__main__':
    app.run(debug=True)

#################################################
# Dependencies
#################################################
import numpy as np

from flask import Flask, render_template, jsonify, redirect

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, func, inspect, Column, Integer, String

import os
from flask_sqlalchemy import SQLAlchemy

import databaseEngineering
from dataEngineering import *

#################################################
# Create Databases
#################################################
createDatabase()

#################################################
# Engine Setup
#################################################
engine = create_engine('postgres://lqehqdnexeuwdi:e299f2b76843b838b81976e7cb183859f28b1cd99e6aa417fdce1340ce00fece@ec2-54-243-210-70.compute-1.amazonaws.com:5432/dbenqc5p6hbe3e')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
Base = automap_base()
Base.metadata.reflect(engine)

#################################################
# Engine Setup
#################################################

# engine = create_engine('sqlite:///data/data.sqlite')
engine = create_engine('postgres://lqehqdnexeuwdi:e299f2b76843b838b81976e7cb183859f28b1cd99e6aa417fdce1340ce00fece@ec2-54-243-210-70.compute-1.amazonaws.com:5432/dbenqc5p6hbe3e')

Base = automap_base()
Base.prepare(engine, reflect=True)

#################################################
# Add Tables from DFs
#################################################
# Create cleaned dataframes from raw sources:
ucrData = ucrData()
choroplethCoordsData = choroplethCoords()
schoolShootingsData = schoolShootings()

#################################################
# Session Setup
#################################################
session = scoped_session(sessionmaker(bind=engine))

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Full dashboard
@app.route('/')
def index():
    """Return the dashboard homepage."""

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

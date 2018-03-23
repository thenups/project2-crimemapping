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

#################################################
# Engine Setup
#################################################
engine = create_engine('sqlite:///data/data.sqlite')
# engine = create_engine('postgres://lqehqdnexeuwdi:e299f2b76843b838b81976e7cb183859f28b1cd99e6aa417fdce1340ce00fece@ec2-54-243-210-70.compute-1.amazonaws.com:5432/dbenqc5p6hbe3e')
Base = declarative_base()
Base.metadata.reflect(engine)

#################################################
# Database Setup
#################################################
class Metadata(Base):
    __table__ = Base.metadata.tables['ucr']ucr

class Samples(Base):
    __table__ = Base.metadata.tables['state_coordinates']

#################################################
# Session Setup
#################################################
session = scoped_session(sessionmaker(bind=engine))

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

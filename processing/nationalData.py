#################################################
# Dependencies
#################################################
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base #classes into tables
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, func, inspect, Column, Integer, String

import psycopg2
import os

#################################################
# Engine Setup
#################################################
engine = create_engine(os.environ.get('DATABASE_URL', '') or 'postgres://lqehqdnexeuwdi:e299f2b76843b838b81976e7cb183859f28b1cd99e6aa417fdce1340ce00fece@ec2-54-243-210-70.compute-1.amazonaws.com:5432/dbenqc5p6hbe3e')

#################################################
# Save reference to each table in database
#################################################
Base = declarative_base()
Base.metadata.reflect(engine)

#################################################
# Session Setup
#################################################
session = Session(bind=engine)


def unpackTuples(results):
    cleanedResults = []

    # Unpack tuple
    for i in results:
        cleanedResults.append(float(i[0]))

    return cleanedResults

def ifSnap(dataset):

    class Snap(Base):
        __table__ = Base.metadata.tables['snap']

    sel = [Snap.average_participation]

    results = session.query(*sel).\
              filter(Snap.year>2003).\
              filter(Snap.year<2015).all()

    return unpackTuples(results)

def ifForeclosure(dataset):
    class Foreclosure(Base):
        __table__ = Base.metadata.tables['foreclosure']

    sel = [Foreclosure.foreclosure_filings]

    results = session.query(*sel).\
              filter(Foreclosure.year>2003).\
              filter(Foreclosure.year<2015).all()

    return unpackTuples(results)

def getValues(dataset):
    # Model table
    class DB(Base):
        __table__ = Base.metadata.tables[dataset]

    sel = []

    # Select and sum year columns in database
    for i in range(2004,2015):
        col = getattr(DB,str(i))
        sel.append(func.sum(col))

    # Query database
    results = session.query(*sel).all()

    cleanedResults = []

    # Unpack tuple
    for i in results[0]:
        cleanedResults.append(float(i))

    return cleanedResults

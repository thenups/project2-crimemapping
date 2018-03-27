#################################################
# Dependencies
#################################################
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, MetaData, func #connect to database
# from sqlalchemy.ext.declarative import declarative_base #classes into tables
# from sqlalchemy import Column, Integer, String, Float, Date #allow us to declare column typs
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
# import pymysql
from data.dataEngineering import choroplethCoords, ucrData, schoolShootings

def write_databases():
    #################################################
    # Engine Setup
    #################################################
    # engine = create_engine('sqlite:///data/data.sqlite', convert_unicode=True, echo=False)
    # engine = create_engine('postgres://lqehqdnexeuwdi:e299f2b76843b838b81976e7cb183859f28b1cd99e6aa417fdce1340ce00fece@ec2-54-243-210-70.compute-1.amazonaws.com:5432/dbenqc5p6hbe3e')
    engine = create_engine('postgres://lqehqdnexeuwdi:e299f2b76843b838b81976e7cb183859f28b1cd99e6aa417fdce1340ce00fece@ec2-54-243-210-70.compute-1.amazonaws.com:5432/dbenqc5p6hbe3e')

    # Create connection
    conn = engine.connect()

    #################################################
    # Add Tables from DFs
    #################################################
    # Create cleaned dataframes from raw sources:
    vcrData = ucrData('raw/ucr_violent_crime_rate_by_state.csv')
    choroplethCoordsData = choroplethCoords()
    schoolShootingsData = schoolShootings()

    # Convert DF into DB tables (and create primary key)
    # conn.execute('DROP TABLE IF EXISTS vcr;')
    ucrData.to_sql(name='vcr', con=engine, if_exists = 'replace', index=True)
    conn.execute('ALTER TABLE vcr ADD PRIMARY KEY (index);')

    # conn.execute('DROP TABLE IF EXISTS state_coordinates;')
    choroplethCoordsData.to_sql(name='state_coordinates', con=engine, if_exists = 'replace', index=True)
    conn.execute('ALTER TABLE state_coordinates ADD PRIMARY KEY (index);')

    # conn.execute('DROP TABLE IF EXISTS school_shootings;')
    schoolShootingsData.to_sql(name='school_shootings', con=engine, if_exists = 'replace', index=True)
    conn.execute('ALTER TABLE school_shootings ADD PRIMARY KEY (index);')

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
from data.dataEngineering import choroplethCoords, ucrData, schoolShootings, foreclosureData, snapData

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
    # Create cleaned dataframes from raw sources
    # Convert DF into DB tables (and create primary key)

    #### VIOLENT CRIME RATE ####
    vcrData = ucrData('raw/ucr_violent_crime_rate_by_state.csv')
    vcrData.to_sql(name='vcr', con=engine, if_exists ='replace', index=False)
    conn.execute('ALTER TABLE vcr ADD PRIMARY KEY ("stateId");')
    ####################

    #### VIOLENT CRIME ####
    violentCrimeData = ucrData('raw/ucr_violent_crime_total.csv')
    violentCrimeData.to_sql(name='violent_crime', con=engine, if_exists = 'replace', index=False)
    conn.execute('ALTER TABLE violent_crime ADD PRIMARY KEY ("stateId");')
    ####################

    #### MURDER ####
    murderData = ucrData('raw/ucr_murder_and_nonnegligent_manslaughter.csv')
    murderData.to_sql(name='murder', con=engine, if_exists = 'replace', index=False)
    conn.execute('ALTER TABLE murder ADD PRIMARY KEY ("stateId");')
    ####################

    #### UNEMPLOYMENT ####
    unemploymentData = ucrData('raw/clean_unemployment_by_state.csv')
    unemploymentData.to_sql(name='unemployment', con=engine, if_exists ='replace', index=False)
    conn.execute('ALTER TABLE unemployment ADD PRIMARY KEY ("stateId");')
    ####################

    #### POPULATION ####
    populationData = ucrData('raw/clean_population_by_year.csv')
    populationData.to_sql(name='population', con=engine, if_exists = 'replace', index=False)
    conn.execute('ALTER TABLE population ADD PRIMARY KEY ("stateId");')
    ####################

    #### STATE COORDINATES ####
    choroplethCoordsData = choroplethCoords()
    choroplethCoordsData.to_sql(name='state_coordinates', con=engine, if_exists='replace', index=True)
    conn.execute('ALTER TABLE state_coordinates ADD PRIMARY KEY (index);')
    ################

    #### SCHOOL SHOOTINGS ####
    schoolShootingsData = schoolShootings()
    schoolShootingsData.to_sql(name='school_shootings', con=engine, if_exists='replace', index=True)
    conn.execute('ALTER TABLE school_shootings ADD PRIMARY KEY (index);')
    ####################

    #### FORECLOSURES ####
    foreclosureData = foreclosureData()
    foreclosureData.to_sql(name='foreclosure', con=engine, if_exists = 'replace', index=True)
    conn.execute('ALTER TABLE foreclosure ADD PRIMARY KEY (index);')
    ####################

    #### SNAP ####
    snapData = snapData()
    snapData.to_sql(name='snap', con=engine, if_exists = 'replace', index=True)
    conn.execute('ALTER TABLE snap ADD PRIMARY KEY (index);')
    ####################

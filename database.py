# Dependencies
import pandas as pd
from datetime import datetime
import sqlalchemy
from sqlalchemy import create_engine, MetaData, func #connect to database
from sqlalchemy.ext.declarative import declarative_base #classes into tables
from sqlalchemy import Column, Integer, String, Float, Date #allow us to declare column typs
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
import pymysql

# starts creating connection from Python to SQL database
pymysql.install_as_MySQLdb()


# Create a reference the CSV file
crimByJuridsdiction = 'cleaned_crime_by_jurisdiction.csv'
schoolShootings = 'cleaned_school_shootings_1990_2018.csv'
violentCrimeRate = 'ucr_violent_crime_rate_by_state_expanded.csv'

# Load the cleaned csv file into a pandas dataframe
# measurementDF = pd.read_csv(measurementFile)
# measurementDF['date'] = pd.to_datetime(measurementDF['date']) #change date column to datetime
# stationDF = pd.read_csv(stationFile)

# Use Orient='records' to create a list of data to write
# to_dict() cleans out DataFrame metadata as well
# measurementData = measurementDF.to_dict(orient='records')
# stationData = stationDF.to_dict(orient='records')


# Create our database engine
engine = create_engine('sqlite:///crime.sqlite')
conn = engine.connect()

# Create base
Base = declarative_base() #object that utilizes the default for declarative base
#
# # Create ORM classes
# class Measurement(Base):
#     __tablename__='measurement'
#     id = Column(Integer, primary_key=True)
#     station = Column(String(255))
#     date = Column(Date)
#     prcp = Column(Float(5,5))
#     tobs = Column(Integer)
#
#     def __repr__(self):
#         return f'id={self.id},station={self.station},date={self.date},prcp={self.prcp},tobs={self.tobs}'
#
# #format='%Y-%m-%d'
#
# class Station(Base):
#     __tablename__='station'
#     id = Column(Integer, primary_key=True)
#     station = Column(String(255))
#     name = Column(String(255))
#     latitude = Column(Float(3,5))
#     longitude = Column(Float(3,5))
#     elevation = Column(Integer)
#
#     def __repr__(self):
#         return f"id={self.id},station={self.station},name={self.name},latitude={self.latitude},longitude={self.longitude},elevation={self.elevation}"

# Use MetaData from SQLAlchemy to reflect the tables
metadata = MetaData(bind=engine)
metadata.reflect()

# Use a Session to test the classes
Base.metadata.create_all(engine)
session = Session(bind=engine)

# Save the reference to the sqlite tables as a variables
measurementTable = sqlalchemy.Table('measurement', metadata, autoload=True)
stationTable = sqlalchemy.Table('station', metadata, autoload=True)

# Use `table.delete()` to remove any pre-existing data.
# conn.execute(measurementTable.delete())
conn.execute(stationTable.delete())

# Use `table.insert()` to insert the data into the table
# The SQL table is populated during this step
conn.execute(measurementTable.insert(), measurementData)
conn.execute(stationTable.insert(), stationData)

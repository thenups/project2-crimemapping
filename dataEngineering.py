#################################################
# Dependencies
#################################################
import pandas as pd
import numpy as np
import requests
import json

# Create UCR DF
def ucrData():
    # Read files into dataframes
    filepath = 'data/raw/ucr_violent_crime_rate_by_state.csv'
    csv = pd.read_csv(filepath)
    df = pd.DataFrame(csv)

    # Transpose data
    df = df.set_index('Year').T
    # reset index name and reset index
    df.index.names = ['State']
    df = df.reset_index()

    df.to_dict(orient='records')

    return df

# Create cloropleth DF
def choroplethCoords():
    # Get template
    coordinateJSON = requests.get('http://eric.clst.org/assets/wiki/uploads/Stuff/gz_2010_us_040_00_20m.json').json()

    # Create lists to insert into dataframe
    stateType = []
    stateID = []
    stateName = []
    geometry = []

    # Add data from JSON into lists
    for feature in coordinateJSON['features']:
        stateType.append(feature['type'])
        stateID.append(feature['properties']['STATE'])
        stateName.append(feature['properties']['NAME'])
        geometry.append(feature['geometry'])

    # Create dictionary for DF
    allCoords = {
        'stateType' : stateType,
        'stateId' : stateID,
        'stateName' : stateName,
        'geometry' : str(geometry)
        }

    # Create DF
    coordsDF = pd.DataFrame(data=allCoords)

    return coordsDF

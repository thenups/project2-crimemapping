# Dependencies

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
        'type' : stateType,
        'stateid' : stateID,
        'stateName' : stateName,
        'geometry' : geometry
        }

    # Create DF
    coordsDF = pd.DataFrame(data=allCoords)

    return coordsDF

def pointCoords():

    # Google GEOcode API constants
    api_key = 'AIzaSyBqwyQMdmH_-LZRLxrnLgtlzfenQiV0uoI'
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    example_url_new_york = 'https://maps.googleapis.com/maps/api/geocode/json?address=New%20York&region=New%20York&key=AIzaSyBqwyQMdmH_-LZRLxrnLgtlzfenQiV0uoI'

    # Read in CSV and create dataframe
    filepath = "data/raw/school_shootings_1990_2018.csv"
    csv = pd.read_csv(filepath)
    df = pd.DataFrame(csv)

    # Remove duplicates (True in Dupe column if record is duplicate)
    df.drop(df[df['Dupe'] == True].index, inplace=True)
    df = df.reset_index(drop=True)

    # Remove superfluous columns
    skinny_df = df[['Date', 'City', 'State', 'Fatalities']]


    # --Parse date and add year column for later manipulation:--

    # Create new column
    skinny_df['Year'] = ''

    # iterate over rows
    for index, row in skinny_df.iterrows():
        # grab last two digits of date field, cast as int, store
        date = int(row['Date'][-2:])
        # if date is under 20, make it 20xx, else 19xx and set that to the row we are on, under Year column
        if (date < 20):
            skinny_df.iat[index, 4] = int(date + 2000)
        else:
            skinny_df.iat[index, 4] = int(date + 1900)
    

    # --add lat, long columns using google maps geocode API:--
    
    # extracts city, state from dataframe, calls API, traverses resulting json and sets new columns to returned values
    # note: code takes about 5 minutes to run (API calls)

    for index, row in skinny_df.iterrows():
        city = row['City']
        state = row['State']
        url = base_url + 'address=' + city + '&region=' + state + '&key=' + api_key
        json = requests.get(url).json()
        lat = json['results'][0]['geometry']['location']['lat']
        lng = json['results'][0]['geometry']['location']['lng']
        skinny_df.loc[index, 'Latitude'] = lat
        skinny_df.loc[index, 'Longitude'] = lng

    cleaned_dataframe = skinny_df

    return cleaned_dataframe
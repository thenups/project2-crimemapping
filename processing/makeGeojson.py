#################################################
# Dependencies
#################################################
import numpy as np
import requests
import json

def choropleth_geojson(resultList,year):

    features = []

    for n in l:
        features.append(
            {
                'type': 'Feature',
                'properties': {
                    'STATE': n[0],
                    'VCR': n[3],
                    'YEAR': int(y)
                },
            'geometry': {
                'type': n[1],
                'coordinates': json.loads(n[2])
            }
        }
    )

    geoJSON = {
        'type': 'FeatureCollection',
        'features': features
    }

    return (geoJSON)


def shootings_geoJSON(table_returned_from_sqlite_postgres):
    # create empty list to hold all geoJSON feature objects
    feature_list = []

    # iterate through rows from sqlite/postgres query !!! REMOVE key, value AND .items() AFTER TESTING FUNCTION !!!
    for row in table_returned_from_sqlite_postgres:

        # extract relevant data, and store
        year_in_question = row.Year
        latitude_in_question = row.Latitude
        longitude_in_question = row.Longitude
        fatalities_in_question = row.Fatalities
        city_in_question = row.City
        state_in_question = row.State
        date_in_question = row.Date

        # construct feature object
        # note: coordinate syntax goes long, lat; not lat, long
        new_geoJSON_feature_object = {"type": "Feature",
                                      "properties": {"YEAR": year_in_question,
                                                     "FATALITIES": fatalities_in_question,
                                                     "CITY": city_in_question,
                                                     "STATE": state_in_question,
                                                     "DATE": date_in_question},
                                      "geometry": {"type": "Point",
                                                   "coordinates": [longitude_in_question, latitude_in_question]}
                                     }

        # append new feature object to feature_list
        feature_list.append(new_geoJSON_feature_object)

        # create collection to hold all state geoJSON feature objects to hand to mapbox as the geoJSON source
    geoJSON_collection = {"type": "FeatureCollection",
                          "features": feature_list}

    return geoJSON_collection

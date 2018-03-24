#################################################
# Dependencies
#################################################
import numpy as np
import requests
import json

def choropleth_geojson(l):

    features = []

    for n in l:
        features.append(
            {
                'type': 'Feature',
                'properties': {
                    'state': n[0],
                    'vcr': n[3]
                },
            'geometry': {
                'type': n[1],
                'coordinates': n[2]
            }
        }
    )

    geoJSON = {
        'type': 'FeatureCollection',
        'features': features
    }

    return (geoJSON)

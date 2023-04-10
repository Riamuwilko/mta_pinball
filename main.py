import sqlite3
import json
import os
import requests

def load_jsons(url,params):
    response = requests.get(url, params=params)
    data = json.loads(response.content.decode('utf-8'))
    return data

def write_json(filename, data):
    json_object = json.dumps(data,indent=4)
    with open(filename,"w") as outfile:
        outfile.write(json_object)

def main():
    #Setting up to use the api
    api_key = "ac48cdfe-09b7-42f6-95eb-9415ec1ae408"
    route_id = "MTA NYCT_M1"
    url = 'https://bustime.mta.info/api/where/stops-for-route/MTA NYCT_M1.json'

    #Setting up the parameters
    params = {
        'key': api_key,
        'version': '2',
        'id': route_id,
        'includePolylines': 'false'
    }
   
    data_dict = load_jsons(url,params)

    #Setting up to load all the info about the bus back into json
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filename = dir_path + '/' + "bus.json"
    write_json(filename,data_dict)

if __name__ == '__main__':
    main()
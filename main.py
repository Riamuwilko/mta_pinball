import sqlite3
import json
import os
import requests
import matplotlib.pyplot as plt

def load_jsons(url,params):
    response = requests.get(url, params=params)
    data = json.loads(response.content.decode('utf-8'))
    return data

def write_json(filename, data):
    json_object = json.dumps(data,indent=4)
    with open(filename,"w") as outfile:
        outfile.write(json_object)

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_tables(cur, conn):
    # Create MTA table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Mta "
        "(stop_id INTEGER PRIMARY KEY, route_id INTEGER, lat INTEGER, lon INTEGER) "
    )
    

    # Create pinball table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Pinball "
        "(pinball_id INTEGER PRIMARY KEY, lat INTEGER, lon INTEGER) "
    )

    # Create ___ table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS "
        "() "
    )

    # Commit changes
    conn.commit()

def find_pinball(cur, conn):
    # Pick a stop

    # Determine how close to the stop to search

    # Set up api

    # Make request to api

    # Retrieve json data

    # Insert into db

    pass

def main():
    # Set up database cursor and connection
    cur, conn = open_database('pinball.db')

    # Create tables
    create_tables(cur, conn)

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

    # Retrieve pinball information
    find_pinball(cur, conn)

    # Calculate

if __name__ == '__main__':
    main()
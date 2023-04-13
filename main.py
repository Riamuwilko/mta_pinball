import sqlite3
import json
import os
import requests
import re

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
        "(stop_id INTEGER PRIMARY KEY, route_id INTEGER, lat INTEGER, lon INTEGER, arcade_id INTEGER FOREIGN KEY) "
    )
    
    # Create arcades table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Arcades "
        "(arcade_id INTEGER PRIMARY KEY, name TEXT, lat INTEGER, lon INTEGER) "
    )

    # Create pinball table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Pinball "
        "(machine_id INTEGER PRIMARY KEY, name TEXT, year INTEGER, arcade_id INTEGER FOREIGN KEY) "
    )

    # Commit changes
    conn.commit()

def find_pinball(cur, conn):
    # Pick a stop
    cur.execute(
        "SELECT stop_id, lat, lon "
        "FROM Mta "
        "WHERE arcade_id IS NULL "
    )
    stop = cur.fetchone()
    stop_id = stop[0]
    lat = stop[1]
    lon = stop[2]

    # Set up api
    url = "https://pinballmap.com/api/v1/locations/closest_by_lat_lon.json"

    # Make request to api
    params = {
        "lat": lat,
        "lon": lon
    }
    response = requests.get(url, params)

    # Retrieve json data
    data = response.text
    info = json.loads(data)
    location = info["location"]

    # Add the arcade location
    cur.execute(
        "INSERT OR IGNORE INTO Arcades "
        "(arcade_id, name, lat, lon) "
        "VALUES (?, ?, ?, ?) ",
        (location["id"], location["name"], location["lat"], location["lon"])
    )

    # Update the stop's nearest arcade
    cur.execute(
        "UPDATE Mta "
        "SET arcade_id = ? "
        "WHERE stop_id = ? ",
        (location["id"], stop_id)
    )

    # Get info about pinball machines
    # Only get information about the first x machines at each arcade
    count = 24
    if len(location["machine_ids"]) < count:
        count = len(location["machine_ids"])
    
    # Insert pinball machine information
    m_names = location["machine_names"]
    m_ids = location["machine_ids"]
    for i in range(count):
        # Grab the year from the name
        year = re.findall(r", \d{4}\)", m_names[i]).strip(",)")

        # Insert pinball information
        cur.execute(
            "INSERT OR IGNORE INTO Pinball "
            "(machine_id, name, year, arcade_id) "
            "VALUES (?, ?, ?, ?) ",
            (m_ids[i], m_names[i], int(year), location["id"])
        )

    conn.commit()

def print_stats(cur, conn):
    cur.execute("SELECT COUNT(stop_id) FROM Mta")
    num_stops = cur.fetchone[0]

    cur.execute("SELECT COUNT(arcade_id) FROM Arcades")
    num_arcades = cur.fetchone[0]

    cur.execute("SELECT COUNT(machine_id) FROM Pinball")
    num_machines = cur.fetchone[0]

    total = num_arcades + num_machines + num_stops
    print(f"Number of MTA Stops: {num_stops}")
    print(f"Number of Arcades: {num_arcades}")
    print(f"Number of Pinball machines: {num_machines}")
    print(f"Total rows in database: {total}")

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

    # Print out database information
    print_stats(cur, conn)

if __name__ == '__main__':
    main()
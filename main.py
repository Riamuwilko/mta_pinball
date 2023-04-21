import sqlite3
import json
import os
import requests
import re


def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def create_tables(cur, conn):

    # Create arcades table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Arcades "
        "(arcade_id INTEGER PRIMARY KEY, name TEXT, lat INTEGER, lon INTEGER, number_of_pinball INTEGER) "
    )

    # Create MTA table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Mta "
        "(stop_id INTEGER PRIMARY KEY, route_id TEXT, lat INTEGER, lon INTEGER, arcade_id INTEGER) "
    )

    # Create pinball table
    cur.execute(
        "CREATE TABLE IF NOT EXISTS Pinball "
        "(machine_id INTEGER PRIMARY KEY, name TEXT, year INTEGER, arcade_id INTEGER) "
    )

    # Commit changes
    conn.commit()


def find_stop(cur, conn):
    m1_counter = 5
    q58_counter = 5
    q44_counter = 5
    b14_counter = 5
    s40_counter = 5
    # Setting up to use the api
    api_key = "ac48cdfe-09b7-42f6-95eb-9415ec1ae408"
    m1_url = 'https://bustime.mta.info/api/where/stops-for-route/MTA NYCT_M1.json'
    q58_url = 'https://bustime.mta.info/api/where/stops-for-route/MTA NYCT_Q58.json'
    q44_url = 'https://bustime.mta.info/api/where/stops-for-route/MTA NYCT_Q44+.json'
    b14_url = 'https://bustime.mta.info/api/where/stops-for-route/MTA NYCT_B14.json'
    s40_url = 'https://bustime.mta.info/api/where/stops-for-route/MTA NYCT_S40.json'

    # Setting up the parameters
    params = {
        'key': api_key,
        'version': '2',
        'includePolylines': 'false'
    }
    # Retrieve json data
    m1_response = requests.get(m1_url, params=params)
    m1_data = m1_response.text
    m1_info = json.loads(m1_data)

    q58_response = requests.get(q58_url, params=params)
    q58_data = q58_response.text
    q58_info = json.loads(q58_data)

    q44_response = requests.get(q44_url, params=params)
    q44_data = q44_response.text
    q44_info = json.loads(q44_data)

    b14_response = requests.get(b14_url, params=params)
    b14_data = b14_response.text
    b14_info = json.loads(b14_data)

    s40_response = requests.get(s40_url, params=params)
    s40_data = s40_response.text
    s40_info = json.loads(s40_data)

    # Retrieve a list of stops
    m1_stops = m1_info["data"]["references"]["stops"]
    q58_stops = q58_info["data"]["references"]["stops"]
    q44_stops = q44_info["data"]["references"]["stops"]
    b14_stops = b14_info["data"]["references"]["stops"]
    s40_stops = s40_info["data"]["references"]["stops"]

    for i in range(0, len(m1_stops), 2):
        while m1_counter > 0:
            cur.execute(
                "SELECT stop_id "
                "FROM Mta "
                "WHERE Mta.stop_id = ? ",
                (int(m1_stops[i]['code']),)
            )
            result = cur.fetchone()
            if result:
                break
            else:
                # insert
                cur.execute(
                    "INSERT OR IGNORE INTO Mta "
                    "(stop_id,route_id,lat,lon,arcade_id) "
                    "VALUES (?, ?, ?, ?, ?) ",
                    (m1_stops[i]['code'], "MTA NYCT_M1",
                     m1_stops[i]['lat'], m1_stops[i]['lon'], None)
                )
                m1_counter -= 1
                break

    for i in range(0, len(q58_stops), 2):
        while q58_counter > 0:
            cur.execute(
                "SELECT stop_id "
                "FROM Mta "
                "WHERE Mta.stop_id = ? ",
                (int(q58_stops[i]['code']),)
            )
            result = cur.fetchone()
            if result:
                break
            else:
                # insert
                cur.execute(
                    "INSERT OR IGNORE INTO Mta "
                    "(stop_id,route_id,lat,lon,arcade_id) "
                    "VALUES (?, ?, ?, ?, ?) ",
                    (q58_stops[i]['code'], "MTA NYCT_Q58",
                     q58_stops[i]['lat'], q58_stops[i]['lon'], None)
                )
                q58_counter -= 1
                break

    for i in range(0, len(q44_stops), 2):
        while q44_counter > 0:
            cur.execute(
                "SELECT stop_id "
                "FROM Mta "
                "WHERE Mta.stop_id = ? ",
                (int(q44_stops[i]['code']),)
            )
            result = cur.fetchone()
            if result:
                break
            else:
                # insert
                cur.execute(
                    "INSERT OR IGNORE INTO Mta "
                    "(stop_id,route_id,lat,lon,arcade_id) "
                    "VALUES (?, ?, ?, ?, ?) ",
                    (q44_stops[i]['code'], "MTA NYCT_Q44+",
                     q44_stops[i]['lat'], q44_stops[i]['lon'], None)
                )
                q44_counter -= 1
                break

    for i in range(0, len(b14_stops), 2):
        while b14_counter > 0:
            cur.execute(
                "SELECT stop_id "
                "FROM Mta "
                "WHERE Mta.stop_id = ? ",
                (int(b14_stops[i]['code']),)
            )
            result = cur.fetchone()
            if result:
                break
            else:
                # insert
                cur.execute(
                    "INSERT OR IGNORE INTO Mta "
                    "(stop_id,route_id,lat,lon,arcade_id) "
                    "VALUES (?, ?, ?, ?, ?) ",
                    (b14_stops[i]['code'], "MTA NYCT_B14",
                     b14_stops[i]['lat'], b14_stops[i]['lon'], None)
                )
                b14_counter -= 1
                break

    for i in range(0, len(s40_stops), 2):
        while s40_counter > 0:
            cur.execute(
                "SELECT stop_id "
                "FROM Mta "
                "WHERE Mta.stop_id = ? ",
                (int(s40_stops[i]['code']),)
            )
            result = cur.fetchone()
            if result:
                break
            else:
                # insert
                cur.execute(
                    "INSERT OR IGNORE INTO Mta "
                    "(stop_id,route_id,lat,lon,arcade_id) "
                    "VALUES (?, ?, ?, ?, ?) ",
                    (s40_stops[i]['code'], "MTA NYCT_S40",
                     s40_stops[i]['lat'], s40_stops[i]['lon'], None)
                )
                s40_counter -= 1
                break
    conn.commit()


def update_mta(cur, conn):
    counter = 0
    # Pick a stop

    # while there is a stop with null arcade_id and we haven't insert over 25 items
    while True:
        cur.execute(
            "SELECT stop_id, lat, lon "
            "FROM Mta "
            "WHERE arcade_id IS NULL "
        )
        stop = cur.fetchone()
        if stop and counter < 25:
            stop_id = stop[0]
            lat = stop[1]
            lon = stop[2]
            # Set up api
            url = "https://pinballmap.com/api/v1/locations/closest_by_lat_lon.json"

            # Make request to api
            params = {
                "lat": lat,
                "lon": lon,
                "max_distance": 10
            }
            response = requests.get(url, params)

            # Retrieve json data
            data = response.text
            info = json.loads(data)
            location = info["location"]

            # Check if arcade is already in the table
            cur.execute(
                "SELECT arcade_id "
                "FROM Arcades "
                "WHERE arcade_id = ? ",
                (location["id"],)
            )
            result = cur.fetchone()
            # nothing happens
            if result:
                counter += 0
            else:
                counter += 1
            # Add the arcade location regardless
            cur.execute(
                "INSERT OR IGNORE INTO Arcades "
                "(arcade_id, name, lat, lon, number_of_pinball) "
                "VALUES (?, ?, ?, ?, ?) ",
                (location["id"], location["name"], location["lat"], location["lon"], location["num_machines"])
            )

            # Update the stop's nearest arcade
            cur.execute(
                "UPDATE Mta "
                "SET arcade_id = ? "
                "WHERE stop_id = ? ",
                (location["id"], stop_id)
            )
        else:
            break
    conn.commit()


def prefill_pinball(cur, conn):
    preset = 25
    # fill up pinball table with 100 existing data.
    url = "https://pinballmap.com/api/v1/machines.json"
    params = {
        "region_id": 95
    }
    response = requests.get(url, params)

    # Retrieve json data
    data = response.text
    info = json.loads(data)
    machines = info["machines"]

    for machine in machines:
        if preset == 0:
            break;
        cur.execute(
            "SELECT machine_id "
            "FROM Pinball "
            "WHERE Pinball.machine_id = ? ",
            (machine["id"],)
        )
        result = cur.fetchone()
        if result:
            preset += 0
        else:
            id = machine["id"]
            name = machine["name"]
            year = machine["year"]
            cur.execute(
                "INSERT OR IGNORE INTO Pinball "
                "(machine_id, name, year, arcade_id) "
                "VALUES (?, ?, ?, ?) ",
                (id, name, year, None)
            )
            preset -= 1
        
    conn.commit()


def find_pinball(cur, conn):
    count = 25
    cur.execute(
        "SELECT lat, lon "
        "FROM Mta "
    )
    stops = cur.fetchall()
    for stop in stops:
        if count == 0:
            break 
        lat = stop[0]
        lon = stop[1]
        # Set up api
        url = "https://pinballmap.com/api/v1/locations/closest_by_lat_lon.json"

        # Make request to api
        params = {
            "lat": lat,
            "lon": lon,
            "max_distance": 10
        }
        response = requests.get(url, params)

        # Retrieve json data
        data = response.text
        info = json.loads(data)
        location = info["location"]

        # Check if pinball is already in the table
        cur.execute(
            "SELECT machine_id "
            "FROM Pinball "
            "WHERE Pinball.machine_id = ? ",
            (location["id"],)
        )
        result = cur.fetchone()
        if result:
            count += 0
        else:
            # Insert pinball machine information
            m_names = location["machine_names"]
            m_ids = location["machine_ids"]
            num_machine = location["num_machines"]
            if count - num_machine < 0:
                break
            count = count - num_machine

            for i in range(num_machine):
                # Grab the year from the name
                year = re.findall(r", \d{4}\)", m_names[i])[0].strip(",)")

                # Insert pinball information
                cur.execute(
                    "INSERT OR IGNORE INTO Pinball "
                    "(machine_id, name, year, arcade_id) "
                    "VALUES (?, ?, ?, ?) ",
                    (m_ids[i], m_names[i], int(year), location["id"])
                )
    conn.commit()

def print_stats(cur, conn):
    # Count the number of rows in the database
    cur.execute("SELECT COUNT(stop_id) FROM Mta")
    num_stops = cur.fetchone()[0]

    cur.execute("SELECT COUNT(arcade_id) FROM Arcades")
    num_arcades = cur.fetchone()[0]

    cur.execute("SELECT COUNT(machine_id) FROM Pinball")
    num_machines = cur.fetchone()[0]

    total = num_arcades + num_machines + num_stops

    # Print relevant
    print(f"Number of MTA Stops: {num_stops}")
    print(f"Number of Arcades: {num_arcades}")
    print(f"Number of Pinball machines: {num_machines}")
    print(f"Total rows in database: {total}")


def main():
    # Set up database cursor and connection
    cur, conn = open_database('pinball.db')

    # Create tables
    create_tables(cur, conn)

    # Retrieve information from database
    cur.execute("SELECT COUNT(stop_id) FROM Mta")
    num_stops = cur.fetchone()[0]
    cur.execute("SELECT COUNT(machine_id) FROM Pinball")
    num_machines = cur.fetchone()[0]
    cur.execute("SELECT COUNT(arcade_id) FROM Arcades")
    num_arcades = cur.fetchone()[0]

    # Fill up bus_stop
    if num_stops < 100:
        find_stop(cur, conn)
    else:
        if num_arcades == 0:
            update_mta(cur, conn)
        else:
            if num_machines < 100:
                prefill_pinball(cur, conn)
            else:
                find_pinball(cur, conn)

    # Print out database information
    print_stats(cur, conn)


if __name__ == '__main__':
    main()

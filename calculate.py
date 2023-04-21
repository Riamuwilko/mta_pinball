# File for calculations
import os
import sqlite3
import csv

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

#return the route with most pinball machine for the first 20 stops
def selecting_route(cur, conn):
    #join mta and aracde table
     # Execute the SQL query to join the Mta and Arcades tables
    cur.execute(
        "SELECT Mta.route_id, SUM(Arcades.number_of_pinball) as total_pinball "
        "FROM Mta "
        "JOIN Arcades ON Mta.arcade_id = Arcades.arcade_id "
        "GROUP BY Mta.route_id "
        "ORDER BY total_pinball DESC "
        "LIMIT 1"
    )
    
    # Fetch the first row of the result and return the route ID
    result = cur.fetchone()
    max_route = result[0]

    #Grab the lat and lon from the route with the max pinball
    cur.execute(
        "SELECT stop_id, lat, lon FROM Mta WHERE route_id = ? "
        "ORDER BY stop_id ",
        (max_route,)
    )
    with open('lat_lons.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Stop_id', 'Latitude', 'Longitude'])
        writer.writerows(cur.fetchall())
        
    conn.commit()

def avg_pinballs_per_route(cur, conn):
    # Find the number of routes
    cur.execute(
        "SELECT DISTINCT route_id "
        "FROM Mta "
    )
    routes = []
    for row in cur:
        routes.append(row[0])

    # Dictionary of lists of the pinball machines for each route
    machines = {}

    
    for route in routes:
        # Find each arcade
        cur.execute(
            "SELECT P.arcade_id, COUNT(P.machine_id) "
            "FROM Mta M, Pinball P "
            "WHERE route_id = ? "
            "AND M.arcade_id = P.arcade_id "
            "GROUP BY P.arcade_id ",
            (route, )
        )
        route_machines = []
        for row in cur:
            route_machines.append(row[1])
        
        machines[route] = route_machines

    # Calculate averages
    with open("average.txt", "w") as f:
        avgs = []
        for route_id, pinballs in machines.items():
            total = 0
            for pinball in pinballs:
                total += int(pinball)
            avg = total / len(pinballs)
            avgs.append((route_id, avg))
        
        # Sort the averages
        avgs = sorted(avgs, key=lambda x: x[1])
        for avg in avgs:
            # Write calculated information
            f.write(f"{avg[0]},{avg[1]}\n")

def pinball_years(cur, conn):
    # Select all pinball years
    cur.execute(
        "SELECT DISTINCT year, COUNT(*) "
        "FROM Pinball "
        "GROUP BY year "
    )
    years = []
    for row in cur:
        years.append(("'" + str(row[0])[2:], int(row[1])))

    # Sort by year
    #years = sorted(years, key=lambda x: x[0])
    
    # Print information
    with open("years.txt", "w") as f:
        for year in years:
            f.write(f"{year[0]},{year[1]}\n")

def main():
    cur, conn = open_database('pinball.db')
    avg_pinballs_per_route(cur, conn)
    selecting_route(cur,conn)
    pinball_years(cur, conn)

if __name__ == '__main__':
    main()
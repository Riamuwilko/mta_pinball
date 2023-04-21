import os
import matplotlib as plt
import folium
import pandas as pd

# Reads in the lines of a file and returns them as two lists of x and y values
# Assumes the format of the file is "{x value} {y value}"
def read_values(filename):
    x = []
    y = []
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.split()
            x.append(line[0])
            y.append(line[1])
    return x, y

# Creates a bar graph using a list of x and y values
def create_avg_graph(x, y):
    # plt.bar(x, y)
    # plt.title("Average Pinball Machines per Route")
    # plt.xlabel("Route IDs")
    # plt.ylabel("Average Number of Pinball Machines")
    # plt.show()
    pass

def plotting_on_map():
    # Read from file
    df = pd.read_csv('lat_lons.csv')

    # Create a Folium map 
    m = folium.Map(location=[df['Latitude'][0], df['Longitude'][0]], zoom_start=12)

    # Add markers for each location
    for i in range(len(df)):
        folium.Marker([df['Latitude'][i], df['Longitude'][i]]).add_to(m)

    # Display the map
    m.save('map.html')


def main():
    # Read in values from calculated file
    barx, bary = read_values("average.txt")
    # Create bar graph
    create_avg_graph(barx, bary)
    plotting_on_map()

if __name__ == '__main__':
    main()
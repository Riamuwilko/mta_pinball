import os
import matplotlib.pyplot as plt
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
            line = line.split(",")
            x.append(line[0])
            y.append(float(line[1]))
    return x, y

# Creates a bar graph using a list of x and y values
def create_avg_graph(x, y):
    plt.style.use('ggplot')
    plt.bar(x, y, color=["red", "orange", "yellow", "green", "blue"], edgecolor="white")
    plt.title("Average Pinball Machines per Route")
    plt.xlabel("Route IDs")
    plt.ylabel("Average Number of Pinball Machines")
    plt.show()

def create_year_graph(x, y):
    plt.style.use('ggplot')
    plt.figure(figsize=(20, 3))
    plt.bar(x, y, align="center", width=0.5)
    plt.title("Number of Pinball Machines by Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Pinball Machines")
    plt.show()

def plotting_on_map():
    # Read from file
    df = pd.read_csv('lat_lons.csv')

    # Create a Folium map 
    m = folium.Map(location=[df['Latitude'][0], df['Longitude'][0]], zoom_start=12)

    # Add markers for each location, with bus stop ID as a popup
    for i in range(len(df)):
        folium.Marker([df['Latitude'][i], df['Longitude'][i]], popup=df['Stop_id'][i]).add_to(m)

    # Display the map
    m.save('map.html')


def main():
    # Read in values from calculated file
    barx, bary = read_values("average.txt")
    yearx, yeary = read_values("years.txt")
    # Create bar graph
    create_avg_graph(barx, bary)
    create_year_graph(yearx, yeary)
    plotting_on_map()

if __name__ == '__main__':
    main()
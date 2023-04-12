import os
import matplotlib as plt

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
    plt.bar(x, y)
    plt.title("Average Pinball Machines per Route")
    plt.show()

def main():
    # Read in values from calculated file
    barx, bary = read_values("average.txt")
    # Create bar graph
    create_avg_graph(barx, bary)
    pass

if __name__ == '__main__':
    main()
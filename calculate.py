# File for calculations
import os
import sqlite3

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def main():
    avg_pinballs_per_route()
    pass

if __name__ == '__main__':
    main()
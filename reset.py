import sqlite3
import os

def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def main():
    # Set up database cursor and connection
    cur, conn = open_database('pinball.db')

    # Reset the database
    cur.execute("DROP TABLE IF EXISTS Mta")
    cur.execute("DROP TABLE IF EXISTS Arcades")
    cur.execute("DROP TABLE IF EXISTS Pinball")
    conn.commit()

if __name__ == '__main__':
    main()
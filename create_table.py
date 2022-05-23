import sqlite3
from sqlite3 import Error
import sys

def create_connection(db_file):
    """
    Function connects to a database.
    
    Parameters
    ----------
    db_file : rString
        File path to the name of the database you would like to connect to.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
    
def main(book_name):
    database = "/mnt/c/sqlite/db/emotions.db"
    
    sql_create_table = f""" CREATE TABLE IF NOT EXISTS {book_name}_table (
                                    id integer PRIMARY KEY,
                                    paragraph VARCHAR(3000),
                                    paragraph_length,
                                    happy float,
                                    angry float,
                                    surprise float,
                                    sad float,
                                    fear float,
                                    dominant_emotion VARCHAR(50),
                                    log_runtime float
                                    ); """
    
    conn = create_connection(database)
    
    if conn is not None:
        create_table(conn, sql_create_table)
    else:
        print("Error! Cannot create the database connection!")
            
if __name__ == '__main__':
    main(sys.argv[1])
import sys
import sqlite3
import logging
from sqlite3 import Error
from time import perf_counter
import text2emotion as te
from prefect import flow, task

database = "/mnt/c/sqlite/db/emotions.db"
file_logger = logging.getLogger(__name__)
file_logger.setLevel(logging.INFO)

@task
def create_table(book_name):
    """
    Connects to database and then creates a table if one doesn't exist for a specific book.
    Parameters
    ----------
    book_name : String
        String of a book name with a text file of that book.
    Returns
    -------
    None
    """
    sql_create_table = f""" CREATE TABLE IF NOT EXISTS {book_name}_table (
                                id integer PRIMARY KEY,
                                paragraph VARCHAR(3000),
                                paragraph_length int,
                                happy float,
                                angry float,
                                surprise float,
                                sad float,
                                fear float,
                                dominant_emotion VARCHAR(50),
                                log_runtime float
                                ); """

    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)
    
    if conn is not None:
        try:
            c = conn.cursor()
            c.execute(sql_create_table)
            return True
        except Error as e:
            print(e)
    else:
        print("Error! Cannot create the database connection!")

@task
def create_data(book_name):
    """
    Function that parses a text file into paragraphs.
    Parameters
    ----------
    book_name : String
        String of a book name with a text file of that book.
    Return
    ------
    A list of paragraphs.
    """
    paragraphs = []
    
    with open(f'./text_files/{book_name}.txt', 'r', encoding="utf8") as f:
        book_text = f.read()

    tests = book_text.split("\n\n")

    for paragraph in tests:
        paragraphs.append(paragraph.replace("\n", " "))

    print("Number of paragraphs in this book: ", len(paragraphs))

    return paragraphs

@task
def insert_data(table_exists, paragraphs, book_name):
    """
    Insert new values into the weather_table.
    Parameters
    ----------
    conn : conn
    project : string, string, datetime, float
        weather_table values as city_name, state_name, datetime, and temperature
    Returns
    -------
    None
    """
    if table_exists:
        file_handler = logging.FileHandler(f'logs/{book_name}.log')
        file_logger.addHandler(file_handler)

        sql = f'''
            INSERT INTO {book_name}_table (paragraph, paragraph_length, happy, angry, surprise, sad, fear, dominant_emotion, log_runtime)
            VALUES(?,?,?,?,?,?,?,?,?)
            '''

        conn = None
        try:
            conn = sqlite3.connect(database)
        except Error as e:
            print(e)

        for paragraph in paragraphs:
            start_time = perf_counter()

            paragraphs_to_emotions = te.get_emotion(paragraph)
            dominant_emotion = ""

            for val in paragraphs_to_emotions.values():
                if val >= 0.5:
                    dominant_emotion = [k for k, v in paragraphs_to_emotions.items() if v == val and val >= 0.5]

            emotion_results = (paragraph,
                            len(paragraph),
                            paragraphs_to_emotions["Happy"],
                            paragraphs_to_emotions["Angry"],
                            paragraphs_to_emotions["Surprise"],
                            paragraphs_to_emotions["Sad"],
                            paragraphs_to_emotions["Fear"],
                            ", ".join(dominant_emotion),
                            0)

            cur = conn.cursor()
            cur.execute(sql, emotion_results)
            row_id = cur.lastrowid
            conn.commit()

            end_time = perf_counter()
            total_time = end_time - start_time
            try:
                file_logger.info('Paragraph Id: %i, Paragraph Length: %i, Execution Time: %f', row_id, len(paragraph), total_time)
            except Error as e:
                file_logger.error(row_id, e)

            update_sql = f'''
            UPDATE {book_name}_table
            SET log_runtime = ?
            WHERE id = ?
            '''

            cur.execute(update_sql, (total_time, row_id))
        conn.close()

@flow
def main(book_name):
    table_exists = create_table(book_name)
    paragraph_data = create_data(book_name)
    insert_data(table_exists, paragraph_data, book_name)

if __name__ == '__main__':
    main(sys.argv[1])
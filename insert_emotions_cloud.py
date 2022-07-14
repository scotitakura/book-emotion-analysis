import sys
import sqlite3
import logging
import os
from sqlite3 import Error
from time import perf_counter
from datetime import timedelta
from nrclex import NRCLex
from prefect import flow, task
from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import IntervalSchedule
import nltk
nltk.download('punkt')
import mysql.connector

schedule = IntervalSchedule(interval=timedelta(minutes=5))
file_logger = logging.getLogger(__name__)
file_logger.setLevel(logging.INFO)

@task(name="Create a mysql table in google cloud")
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
                                fear int,
                                anger int,
                                anticipation int,
                                trust int,
                                surprise int,
                                positive int,
                                negative int,
                                sadness int,
                                disgust int,
                                joy int,
                                log_runtime float
                                ); """

    cnxn = mysql.connector.connect(user = 'root',
    password = 'emotion-pass',
    host = '35.192.147.157',
    database = 'emotions')

    if cnxn.is_connected():
            print('Connected to MySQL database')
    if cnxn is not None:
        try:
            c = cnxn.cursor()
            c.execute(sql_create_table)
            cnxn.commit()
            return True
        except Error as e:
            print(e)
    else:
        print("Error! Cannot Create the database connection!")

@task(name="Parse book text into array of paragraphs")
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
    
    with open(f'./unproccessed_text_files/{book_name}.txt', 'r', encoding="utf8") as f:
        book_text = f.read()

    tests = book_text.split("\n\n")

    for paragraph in tests:
        paragraphs.append(paragraph.replace("\n", " "))

    print("Number of paragraphs in this book: ", len(paragraphs))

    return paragraphs

@task(name="Get emotion score and write it to database")
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

    print("Creating table")
    if table_exists:
        file_handler = logging.FileHandler(f'logs/{book_name}.log')
        file_logger.addHandler(file_handler)

        sql = f'''
            INSERT INTO {book_name}_table (paragraph, paragraph_length, fear, anger, anticipation, trust, surprise, positive, negative, sadness, disgust, joy, log_runtime)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            '''
        
        emotion_keys = ["fear", "anger", "anticipation", "trust", "surprise", "positive", "negative", "sadness", "disgust", "joy"]

        cnxn = mysql.connector.connect(user = 'root',
                password = 'emotion-pass',
                host = '35.192.147.157',
                database = 'emotions')
        cursor = cnxn.cursor()

        for paragraph in paragraphs:
            start_time = perf_counter()
            text_object = NRCLex(paragraph)
            emotion_scores = text_object.raw_emotion_scores
            
            for key in emotion_keys:
                if key not in emotion_scores.keys():
                    emotion_scores[key] = 0
                    
            emotion_results = (paragraph,
                            len(paragraph),
                            emotion_scores["fear"],
                            emotion_scores["anger"],
                            emotion_scores["anticipation"],
                            emotion_scores["trust"],
                            emotion_scores["surprise"],
                            emotion_scores["positive"],
                            emotion_scores["negative"],
                            emotion_scores["sadness"],
                            emotion_scores["disgust"],
                            emotion_scores["joy"],
                            0)
            print(emotion_results)

            
            cursor.executemany(sql, emotion_results)
            row_id = cursor.lastrowid
            cnxn.commit()

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
            
            cursor.execute(update_sql, (total_time, row_id))
            cnxn.commit()
        cnxn.close.close()

@flow(name = "Emotion Analysis Pipeline")
def main_flow():
    if len(os.listdir(f'./unproccessed_text_files')) > 0:
        book_name = os.listdir(f'./unproccessed_text_files')[0][:-4]
        print(book_name)
        table_exists = create_table(book_name)
        paragraph_data = create_data(book_name)
        insert_data(table_exists, paragraph_data, book_name)
        #os.replace(f'./unproccessed_text_files/{book_name}.txt', f'./text_files/{book_name}.txt')
    elif len(os.listdir(f'./unproccessed_text_files')) == 0:
        print("No text files left to proccess!")

if __name__ == "__main__":
    main_flow()
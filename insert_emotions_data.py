import sys
import sqlite3
from sqlite3 import Error
import text2emotion as te

def main(book_name):
    database = "C:\sqlite\db\emotions.db"

    def create_connection(db_file):
        """
        Function connects to a SQLite database.
        
        Parameters
        ----------
        db_file : String
            File path of the database you would like to connect to.
            
        Return
        ------
        Connection obj or None.
        """
        
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
            
        return conn

    def insert_data(conn, project):
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
        
        sql = f'''
            INSERT INTO {book_name}_table (paragraph, paragraph_length, happy, angry, surprise, sad, fear, dominant_emotion)
            VALUES(?,?,?,?,?,?,?,?)
            '''
        cur = conn.cursor()
        cur.execute(sql, project)
        rowid = cur.lastrowid
        conn.commit()
        return rowid

    def listToString(s):
        str1 = ", "
        return(str1.join(s))

    conn = create_connection(database)

    with open(f'./text_files/{book_name}.txt', 'r', encoding="utf8") as f:
        gatsby = f.read()

    tests = gatsby.split("\n\n")
    paragraphs = []

    for paragraph in tests:
        if paragraph != "------------------------------------------------------------------------":
            paragraphs.append(paragraph.replace("\n", " "))

    print("Number of paragraphs in this book: ", len(paragraphs))

    for paragraph in paragraphs:
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
                        listToString(dominant_emotion))

        insert_data(conn, emotion_results)

if __name__ == '__main__':
    main(sys.argv[1])
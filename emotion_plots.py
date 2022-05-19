import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

conn = sqlite3.connect("/mnt/c/sqlite/db/emotions.db")

def main(book_name):
    sql = f"""SELECT id, happy, angry, surprise, sad, fear FROM {book_name}_table"""
    book_title = book_name.replace("_", " ").title()
    read_data = pd.read_sql(sql, conn)
    def sliding_window(elements, window_size):
        windowed_data = []
        if len(elements) <= window_size:
            return elements
        for i in range(len(elements) - window_size + 1):
            windowed_data.append(elements[i:i+window_size].mean())
        return windowed_data

    data = {
        'sad': sliding_window(read_data.sad, 200),
        'happy': sliding_window(read_data.happy, 200),
        'surprise': sliding_window(read_data.surprise, 200),
        'angry': sliding_window(read_data.angry, 200),
        'fear': sliding_window(read_data.fear, 200)
    }

    #fig, ax = plt.subplots()
    plt.plot(range(1, len(data['sad'])+1), data.sad, labels = data.keys())
    plt.legend(loc='upper left')
    plt.title(book_title)
    plt.savefig(f"{book_name}_chart.png")

if __name__ == '__main__':
    main(sys.argv[1])
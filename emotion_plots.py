import sys
import sqlite3

#import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def plotEmotions(table_name):
    conn = sqlite3.connect('emotions.db')
    c = conn.cursor()
    wordUsed = 'Python Sentiment'
    paragraph = f"SELECT id FROM {table_name}"
    happy = f"SELECT Happy FROM {table_name}"

    print(paragraph, happy)
    graphArray = []

    okay = c.execute(happy)
    print(okay)

    #for row in c.execute(sql, [(wordUsed)]):
    #    startingInfo = str(row).replace(')','').replace('(','').replace('u\'','').replace("'","")
    #    splitInfo = startingInfo.split(',')
    #    graphArrayAppend = splitInfo[2]+','+splitInfo[4]
    #    graphArray.append(graphArrayAppend)

    #datestamp, value = np.loadtxt(graphArray,delimiter=',', unpack=True,
    #                            converters={ 0: mdates.strpdate2num(' %Y-%m-%d %H:%M:%S')})

    fig = plt.figure()

    rect = fig.patch

    ax1 = fig.add_subplot(1,1,1,)
    #plt.plot_date(x=paragraph, y=happy, fmt='b-', label = 'value', linewidth=2)
    #plt.show()

if __name__ == '__main__':
    plotEmotions(sys.argv[1])
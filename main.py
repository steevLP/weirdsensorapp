from gettext import npgettext
import os
import datetime

import numpy
import requests
import sqlite3
import csv
import numpy as np
import matplotlib.pyplot as plt

# downloads all required data from target server
def fetchData(year, month, day):
    # 404 Data response
    empty = '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">'

    # iterates over the current date gotten by datetime.now and compares it agains the current function generated date string
    while str(year).zfill(2) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2) <= str(datetime.datetime.now()):

        # downloads files from sensor.community
        if not os.path.exists(
                "./data/" + str(year).zfill(2) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2) + "-3659.csv"):

            # send request to server
            r = requests.get(
                "https://archive.sensor.community/" + str(year).zfill(2) + "-" + str(month).zfill(2) + "-" + str(day).zfill(
                    2) + "/" + str(year).zfill(2) + "-" + str(month).zfill(2) + "-" + str(day).zfill(
                    2) + "_sds011_sensor_3659.csv", allow_redirects=False)

            # read the first line of incoming data to determin if it is invalid or not
            if r.content.decode("utf-8").split("\n")[0] != empty:
                # write data to file
                open("./data/" + str(year).zfill(2) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2) + "-3659.csv", 'wb').write(r.content)

        # counts the self maintained date up a day and iterates month and year conditionally
        day = day + 1
        # use modul to decide whether a month has 30 or 31 days
        if month % 2 == 0:
            if month == 2:
                # catch edgecase februrary
                if day >= 28:
                    month = month + 1
                    day = 1
                    print("add month")
            elif day >= 31:
                month = month + 1
                day = 1
                print("add month")
        elif month % 2 == 1:
            if day >= 30:
                month = month + 1
                day = 1
                print("add month")
            
        # check if december is through
        if month == 12 and day > 31:
            year = year + 1
            month = 1
            day = 1
            print("add year")


# function used to determin if a required file was already proccessed
def isFileWritten(path, filename):
    file = open(path + '/written.txt').read().splitlines()
    for l in file:
        if filename == str(l):
            return True
    return False

# creates database and handles file storage
def storeindb(c, db, path):
    directory = os.fsencode(path)
    store = open(path + '/written.txt', 'a')
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            written = isFileWritten(path, filename)
            if not written:
                store.write(filename + "\n")
                with open(path + "/" + filename, newline='') as csvfile:
                    data = csv.reader(csvfile, delimiter=';')
                    for row in data:
                        if row[0] == "sensor_id":
                            continue
                        else:
                            todo = numpy.array(
                                [row[0], row[1], row[2], row[3], row[4], row[5].split("T")[0], row[5].split("T")[0], row[6], row[9]])
                            c.execute("INSERT INTO sen_data VALUES (?,?,?,?,?,?,?,?,?)", todo)
                            db.commit()
                    else:
                        continue
            else:
                continue

def main():
    # Software Configuration
    day = 1
    month = 1
    year = 2023
    dbp = "app.db"

    # proccessed data
    p1_averages = {}  # Dictionaries werden angelegt, um ein Datum und den jeweils zu dem Tag gehörenden Durchschnittswert zu speichern.
    p2_averages = {}
    discarded_values = 0  # Variable als anhaltspunkt wie viele Datensätze in der Verarbeitung verworfen werden.
    
    # download data and store them for later use
    fetchData(year, month, day)

    # initialize sqlite database
    dbc = sqlite3.connect(dbp)
    c = dbc.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS sen_data (sensor_id,sensor_type,location,lat,lon,date,time,P1,P2);''')
    storeindb(c, dbc, "./data")

    data = c.execute("SELECT avg(P1), avg(P2), date(date) from sen_data group by date(date);").fetchall()
    dbc.close()

    # proccesses the results coming from the databse
    for i in data:
        # filters all values that are higher then 150
        if float(i[0]) < 150.0:
            # add values to dictionary
            p1_averages[i[2]] = i[0]
            p2_averages[i[2]] = i[1]

    # setup gui and start it
    # Code zur Darstellung des Graphen, der die Durchschnittswerte eines Tages für je P1 und P2 Datensätze veranschaulicht
    dates = list(p1_averages.keys())
    p1_values = list(p1_averages.values())
    p2_values = list(p2_averages.values())

    print(p1_values)

    plt.plot(dates, p1_values, label='PM 1.0')
    plt.plot(dates, p2_values, label='PM 2.5')
    plt.xlabel('Datum')
    plt.ylabel('Tagesdurchschnitt in µg/m³')
    plt.title('Messwerte des Staubsensors sds011_3659 im Jahr 2023')
    plt.xticks(rotation=90)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()

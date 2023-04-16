import array
import os
import datetime

import numpy
import requests
import sqlite3
import csv
import sys

from PyQt6 import QtWidgets
import pyqtgraph as pg

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
                open("./data/" + str(year).zfill(2) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2) + "-3659.csv",
                     'wb').write(r.content)

        # counts the self maintained date up a day and iterates month and year conditionally
        day = day + 1
        if day >= 31:
            month = month + 1
            day = 1
            print("add month")
        if month >= 12:
            year = year + 1
            month = 1
            day = 1
            print("add year")

# creates database and handles file storage
def storeindb(c, db, path):
    directory = os.fsencode(path)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            # print(os.path.join(directory, filename))
            with open(path + "/" + filename, newline='') as csvfile:
                data = csv.reader(csvfile, delimiter=';')
                for row in data:
                    print(row)
                    if row[0] == "sensor_id":
                        continue
                    else:
                        todo = numpy.array([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[9]])
                        c.execute("INSERT INTO sen_data VALUES (?,?,?,?,?,?,?,?)",todo)
                        continue
        else:
            continue
    db.commit()

# function for the handling the main window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, d1,d2, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        # plot data: x, y values
        self.graphWidget.plot(d1)


def main():
    # Software Configuration
    day = 1
    month = 1
    year = 2023
    dbp = "app.db"

    # proccessed data
    label = []
    value = []

    # download data and store them for later use
    fetchData(year, month, day)

    # initialize sqlite database
    # delete sqlitedb on each startup
    if os.path.exists(dbp):
        os.remove(dbp)

    # create new database
    dbc = sqlite3.connect(dbp)
    c = dbc.cursor()
    c.execute('''CREATE TABLE sen_data (sensor_id,sensor_type,location,lat,lon,timestamp,P1,P2);''')

    storeindb(c, dbc, "./data")

    data = c.execute("SELECT P1 from sen_data;").fetchall()
    dbc.close()

    # proccesses the results coming from the databse
    for i in data:
        # filters all values that are higher then 100
        if float(i[0]) < 100.0:
            value += [float(i[0])]

    # plt.plot(label, value)
    # plt.show()

    # setup gui and start it
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow(value, [])
    main.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

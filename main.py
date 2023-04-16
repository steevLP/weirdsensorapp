import os
import datetime
import requests
import sqlite3
import csv
import sys

from PyQt6 import QtWidgets
from pyqtgraph import PlotWidget, plot
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
#def storeindb(dbp):
    # sensor_id;sensor_type;location;lat;lon;timestamp;P1;durP1;ratioP1;P2;durP2;ratioP2
    # 3659;SDS011;1846;51.482;7.224;2023-01-01T00:02:05;19.93;;;10.50;;
    # c.execute('''CREATE TABLE sen_data (sensor_id;sensor_type;location;lat;lon;timestamp;P2)''')

    # c.execute("INSERT INTO sen_data VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # db.commit()
    # db.close()

# function for the handling the main window
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, d1,d2, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        hour = d1
        temperature = d2

        # plot data: x, y values
        self.graphWidget.plot(hour, temperature)


def main():
    # Software Configuration
    day = 1
    month = 1
    year = 2023
    dbp = "app.db"

    # initialize sqlite database
    # delete sqlitedb on each startup
    if os.path.exists(dbp):
        os.remove(dbp)

    # create new database
    db = sqlite3.connect(dbp)

    # import dataset
    c = db.cursor()

    # download data and store them for later use
    fetchData(year, month, day)

    # proccessed data
    label = [1,2,3,4,5,6,7,8,9,10]
    value = [30,32,34,32,33,31,29,32,35,45]


    # setup gui and start it
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow(label,value)
    main.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

from gettext import npgettext
import sys
import pandas as pd
from clint.textui import progress
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt
from data import storeindb
from path import writeToFile
from utils import cliProgress
from web import fetchData
from db import makeRequest, initDB

def main():
    # Software Configuration
    fromDate = datetime.strptime("2023-01-01", '%Y-%m-%d').date()
    toDate = datetime.now()
    dbp = "app.db"
    sensor = "3659"
    dataLocation = "./data/"
    dbc = None # stores the created database connection 
    cursor = None # stores database cursor

    # proccessed data
    # dictionary used to store date + average of that date
    p1_averages = {}  
    p2_averages = {}
    

    sensor = input("input sensor id:")
    fromDate = datetime.strptime(input("add date to start tracking from (formate: yyyy/mm/dd): "), '%Y-%m-%d').date()
    toDate = datetime.strptime(input("add date to stop tracking on (formate: yyyy/mm/dd): "), '%Y-%m-%d').date()


    # check if directory exists
    if not os.path.exists(dataLocation):
        os.makedirs(dataLocation)

    if not os.path.exists(dataLocation + "/written.txt"):
        writeToFile(dataLocation, "/written.txt", "")

    daysTotal = (toDate-fromDate).days
    progressed = 0

    # iterates over the current date gotten by datetime.now and compares it agains the current function generated date string
    print("downloading files from server")
    while fromDate <= toDate:
        cliProgress(progressed, daysTotal)
        progressed = progressed + 1
        # download data and store them for later use
        fetchData(str(fromDate), sensor, dataLocation)

        # counts the self maintained date up a day and iterates month and year conditionally
        fromDate = fromDate + timedelta(days=1)
    print("\n")

    # initialize sqlite database
    dbc,c = initDB(dbp)
    makeRequest(c, '''CREATE TABLE IF NOT EXISTS sen_data (sensor_id,sensor_type,location,lat,lon,date,time,P1,P2);''')
    
    print("writing files to database") # spacer to make console output look nicer
    storeindb(c, dbc, "./data")
    print("\n")
    # fetching averages for values P1, P2 and Dates from sqlite database
    data = makeRequest(c, "SELECT avg(P1), avg(P2), date(date) from sen_data group by date(date);").fetchall()
    dbc.close()

    # proccesses the results coming from the databse
    print("preparing data for display")
    progressed = 0
    for i in data:
        # filters all values that are higher then 150
        if float(i[0]) < 150.0:
            # add values to dictionary
            p1_averages[i[2]] = i[0]
            p2_averages[i[2]] = i[1]
            cliProgress(progressed, len(data))
            progressed = progressed + 1
    print("\n")

    dates = list(p1_averages.keys())
    p1_values = list(p1_averages.values())
    p2_values = list(p2_averages.values())

    # setup gui and start it
    # utilizing the native GUI of matplotlib to display values for P1 and P2 
    print("showing data") # spacer to make console output look nicer
    plt.plot(dates, p1_values, label='PM 1.0')
    plt.plot(dates, p2_values, label='PM 2.5')
    plt.xlabel('Datum')
    plt.xticks(rotation=90)
    plt.ylabel('Tagesdurchschnitt in µg/m³')
    plt.title('Messwerte des Staubsensors sds011_'+str(sensor)+' im Jahr 2023')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()

import os.path

import downloader
import datetime
import sqlite3
import csv


print(datetime.datetime.now())
day = 1
month = 1
year = 2023
db = "app.db"
print(str(year).zfill(2) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2))
print(str(year).zfill(2) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2) != str(datetime.datetime.now()))

# iterates over the current date gotten by datetime.now and compares it agains the current function generated date string
while str(year).zfill(2) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2) <= str(datetime.datetime.now()):
    print(str(year).zfill(2) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2))

    # downloads files from sensor.community
    if not os.path.exists("./data/"+str(year).zfill(2) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)+"-3659.csv"):
        downloader.dl("https://archive.sensor.community/"+str(year).zfill(2) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)+"/"+str(year).zfill(2) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)+"_sds011_sensor_3659.csv", "./data/"+str(year).zfill(2) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)+"-3659.csv")

    # counts the selfmaintained date up a day and iterates month and year conditionally
    day = day+1
    if day >= 31:
        month = month+1
        day = 1
        print("add month")
    if month >= 12:
        year = year+1
        month = 1
        day = 1
        print("add year")

# delete sqlitedb on each startup
if os.path.exists(db):
  os.remove(db)

# import dataset

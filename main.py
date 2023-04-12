import os
import datetime
import requests
import sqlite3
import tkinter as tk
import matplotlib.pyplot as plt
import csv

# Software Configuration
day = 1
month = 1
year = 2023
dbp = "app.db"
windows = tk.Tk()

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

# delete sqlitedb on each startup
if os.path.exists(dbp):
    os.remove(dbp)

# create new database
db = sqlite3.connect(dbp)

# import dataset
c = db.cursor()

c.execute('''CREATE TABLE sen_data
             (date text, trans text, symbol text, qty real, price real)''')

c.execute("INSERT INTO sen_data VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

db.commit()
db.close()

# ================================================ #
#                 graph plotting                   #
#                does not work atm                 #
# ================================================ #
fig = plt.figure()

# x axis values
x = [1, 2, 3]
# corresponding y axis values
y = [2, 4, 1]

# plotting the points
plt.plot(x, y)

# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')

# giving a title to my graph
plt.title('My first graph!')

# ================================================================ #
#                            window code                           #
# displays the windows for the frontend i for somereason need      #
# ================================================================ #
greeting = tk.Label(text="Hello, Tkinter")
greeting.pack()
windows.mainloop()
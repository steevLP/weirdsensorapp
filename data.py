import sys
import numpy
import csv
from clint.textui import progress

from os import listdir, fsdecode, fsencode
from path import isFileWritten, writeToFile
from db import makeRequestWithPayload
from sqlite3 import Cursor, Connection

from utils import cliProgress

# creates database and handles file storage
def storeindb(c: Cursor, db: Connection, path: str):
    directory = fsencode(path)
    progressed = 0
    dir = listdir(directory)
    files = len(dir)


    # iterate over files in data directory
    for file in dir:
        filename = fsdecode(file)
        # filter for files that end with .csv
        if filename.endswith(".csv"):
            # check if files already was proccessed
            if not isFileWritten(path, filename):
                # if not note down that it now is
                writeToFile(path, "/written.txt", filename + "\n")
                with open(path + "/" + filename, newline='') as csvfile:
                    data = csv.reader(csvfile, delimiter=';')
                    # filter out first row as it doesnt contain data
                    cliProgress(progressed, files)
                    progressed = progressed + 1

                    for row in data:
                        if row[0] == "sensor_id":
                            continue
                        else:
                            # insert data from row into databse
                            todo = numpy.array([row[0], row[1], row[2], row[3], row[4], row[5].split("T")[0], row[5].split("T")[0], row[6], row[9]])
                            makeRequestWithPayload(c, "INSERT INTO sen_data VALUES (?,?,?,?,?,?,?,?,?)", todo)
                            db.commit()
                    else:
                        continue
            else:
                continue
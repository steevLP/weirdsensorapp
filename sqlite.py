import sqlite3



def InitDB(dbpath):
    db = sqlite3.connect(dbpath)


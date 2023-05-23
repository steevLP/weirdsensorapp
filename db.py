import sqlite3

# initDB creates and connects database
def initDB(path: str):
    try:
        # initialize sqlite database
        dbc = sqlite3.connect(path, timeout=5.0, check_same_thread=False, factory=sqlite3.Connection, cached_statements=128)
        cursor = dbc.cursor()
        return dbc, cursor
    except:
        print("something broke whiles creating a connection")
        # raise TypeError("could not initialize sqlite db")

# makeRequest submits a given sql query string to a given database
def makeRequest(c: sqlite3.Cursor, query: str) -> sqlite3.Cursor:
    try:
        res = c.execute(query)
        if res != None:
            return res
        else:
            raise TypeError("an error occured while performing request: cursor ended up empty")
    except sqlite3.ProgrammingError:
        raise TypeError("an error occured while performing query")
    
# makeRequest submits a given sql query string to a given database
def makeRequestWithPayload(c: sqlite3.Cursor, query: str, payload) -> sqlite3.Cursor:
    try:
        res = c.execute(query, payload)
        if res != None:
            return res
        else:
            raise TypeError("an error occured while performing request: cursor ended up empty")
    except sqlite3.ProgrammingError:
        raise TypeError("an error occured while performing query")
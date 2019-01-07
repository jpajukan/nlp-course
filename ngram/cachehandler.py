import sqlite3

CACHE_DB_LOCATION = "test_data/cache_combined.sqlite3"

def create():
    # If db does not exist then create it
    # Used only when initializing, no further use needed

    conn = sqlite3.connect(CACHE_DB_LOCATION)
    print(sqlite3.version)

    c = conn.cursor()

    c.execute('''CREATE TABLE cache(ngram TEXT, score REAL)''')
    conn.commit()
    conn.close()


def insert_cache(ng, dt):

    conn = sqlite3.connect(CACHE_DB_LOCATION)
    c = conn.cursor()

    #Check before inserting that it does not already exist
    c.execute('SELECT score FROM cache WHERE ngram=?', (ng,))

    row = c.fetchone()
    if row != None:
        conn.close()
        return

    c.execute('insert into cache values (?,?)', (ng, dt))

    conn.commit()
    conn.close()

def get_cache(ng):
    conn = sqlite3.connect(CACHE_DB_LOCATION)
    c = conn.cursor()
    c.execute('SELECT score FROM cache WHERE ngram=?', (ng,))

    row = c.fetchone()

    conn.close()

    if row == None:
        return None

    return row[0]
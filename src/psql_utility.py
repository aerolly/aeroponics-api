import psycopg2
import os
from dotenv import load_dotenv
import simplejson as json
from psycopg2.extras import RealDictCursor

load_dotenv()


############################################################
# Attempt to connect to db
############################################################

conn = psycopg2.connect(
        user = os.environ.get('SQL_USER'),
        password = os.environ.get('SQL_PASS'),
        host = os.environ.get('SQL_IP'),
        port = os.environ.get('SQL_PORT'),
        database = os.environ.get('SQL_DB'))



############################################################
# DB Query Functions
############################################################

# General DB View function
def getResultSetFromDB(funcName, params):
        with conn, conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.callproc(funcName, params)
            result = json.dumps(cursor.fetchall(), default=str)
        return result


# View without js encoding
def getResultSetFromDBNoJS(funcName, params):
        with conn, conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.callproc(funcName, params)
            # Convert from RealDict => json => Python list
            result = json.loads(json.dumps(cursor.fetchall(), default=str))
        return result

# Modify function
def modifyDB(funcName, params):
    with conn, conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.callproc(funcName, params)
        result=json.dumps(cursor.fetchall())

    # Return status and error message
    return result

#############################################################

# Establish connection to DB

def connectDB():
    try:
        conn = psycopg2.connect(
                user = os.environ.get('SQL_USER'),
                password = os.environ.get('SQL_PASS'),
                host = os.environ.get('SQL_IP'),
                port = os.environ.get('SQL_PORT'),
                database = os.environ.get('SQL_DB'))

    except:
        print("Couldn not connect to DB")


# Disconnect from DB
def closeDB():
    try:
        conn.close()
    except:
        print("Unable to close DB connection")
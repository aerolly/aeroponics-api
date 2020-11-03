import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv
import simplejson as json
from psycopg2.extras import RealDictCursor

load_dotenv()


############################################################
# Establish Connection Pool
############################################################

pool = psycopg2.pool.ThreadedConnectionPool(1,10,
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
    conn = pool.getconn()
    with conn, conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.callproc(funcName, params)
        result = json.dumps(cursor.fetchall(), default=str)
    pool.putconn(conn)
    return result


# View without js encoding
def getResultSetFromDBNoJS(funcName, params):
    conn = pool.getconn()
    with conn, conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.callproc(funcName, params)
        # Convert from RealDict => json => Python list
        result = json.loads(json.dumps(cursor.fetchall(), default=str))
    pool.putconn(conn)
    return result


# Modify function
def modifyDB(funcName, params):
    conn = pool.getconn()
    with conn, conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.callproc(funcName, params)
        result=json.dumps(cursor.fetchall())
    pool.putconn(conn)
    # Return status and error message
    return result


# Call at end of application
def closeDB():
    if pool:
        pool.closeall()
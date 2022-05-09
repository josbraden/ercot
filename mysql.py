# MySQL functions for the ercot scraper
# @author Josh Braden

# Imports
import mysql.connector

# DB Variables
dbhost = "127.0.0.1"
dbuser = "dbuser"
dbpasswd = "password"
dbschema = "ercot"
dbcompress = False
# These should be fine unless you also altered the schema file
dbcharset = "utf8mb4"
dbcollation = "utf8mb4_general_ci"


# Function to test database connection
def testMySQL():
    print("Testing database connection...", end='')
    try:
        connection = mysql.connector.connect(
            host=dbhost, user=dbuser, passwd=dbpasswd,
            database=dbschema, compress=dbcompress)

    except mysql.connector.Error as err:
        print(err)
        return -1

    else:
        connection.set_charset_collation(dbcharset, dbcollation)
        connectioncursor = connection.cursor()
        connectioncursor.execute("SELECT COUNT(*) FROM downloads")
        connresult = connectioncursor.fetchone()
        for i in connresult:
            print("Success")

        connectioncursor.close()
        connection.close()
        return 0


# Function to get database existence for a given ercot_doc_id
# Returns 1 if true, 0 if false
def checkDbExistence(ercot_doc_id, table):
    query = "SELECT COUNT(*) FROM "
    query += table
    query += " WHERE ercot_doc_id = "
    query += str(ercot_doc_id)
    try:
        connection = mysql.connector.connect(
            host=dbhost, user=dbuser, passwd=dbpasswd,
            database=dbschema, compress=dbcompress)

    except mysql.connector.Error as err:
        print(err)
        return -1

    else:
        connection.set_charset_collation(dbcharset, dbcollation)
        connectioncursor = connection.cursor()
        connectioncursor.execute(query)
        connresult = connectioncursor.fetchone()
        if connresult[0] == 1:
            ret = 1
        elif connresult[0] == 0:
            ret = 0
        else:
            ret = -1

        connectioncursor.close()
        connection.close()
        return ret
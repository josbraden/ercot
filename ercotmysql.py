# MySQL functions for the ercot scraper
# @author Josh Braden

# Imports
import mysql.connector
from ercotconfig import dbhost, dbuser, dbpasswd, dbschema, dbcompress, dbcharset, dbcollation


# Function to test database connection
def testMySQL():
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
            pass

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


# Function to add a row to the download log table
def addDownload(ercot_report_id, ercot_doc_id, status_code):
    query = "INSERT INTO downloads "
    query += "(ercot_report_id, ercot_doc_id, status_code) VALUES ("
    query += str(ercot_report_id) + "," + str(ercot_doc_id) + "," + str(status_code) + ")"
    try:
        connection = mysql.connector.connect(
            host=dbhost, user=dbuser, passwd=dbpasswd,
            database=dbschema, compress=dbcompress)

    except mysql.connector.Error as err:
        print(err)

    else:
        connection.set_charset_collation(dbcharset, dbcollation)
        connectioncursor = connection.cursor()
        connectioncursor.execute(query)
        connection.commit()
        connectioncursor.close()
        connection.close()


# Function to insert a row to the solar table
def insertSolar(queryData):
    query = "INSERT INTO solar "
    query += "(SYSTEM_WIDE, datetime) VALUES ("
    query += queryData + ")"
    try:
        connection = mysql.connector.connect(
            host=dbhost, user=dbuser, passwd=dbpasswd,
            database=dbschema, compress=dbcompress)
    except mysql.connector.Error as err:
        print(err)
    else:
        connection.set_charset_collation(dbcharset, dbcollation)
        connectioncursor = connection.cursor()
        try:
            connectioncursor.execute(query)
            connection.commit()
        except mysql.connector.errors.IntegrityError:
            # Duplicate entry, ignore
            pass
    finally:
        connectioncursor.close()
        connection.close()


# Function to insert a row to the wind table
def insertWind(queryData):
    query = "INSERT INTO wind "
    query += "(SYSTEM_WIDE, LZ_SOUTH_HOUSTON, LZ_WEST, LZ_NORTH, datetime) VALUES ("
    query += queryData + ")"
    try:
        connection = mysql.connector.connect(
            host=dbhost, user=dbuser, passwd=dbpasswd,
            database=dbschema, compress=dbcompress)
    except mysql.connector.Error as err:
        print(err)
    else:
        connection.set_charset_collation(dbcharset, dbcollation)
        connectioncursor = connection.cursor()
        try:
            connectioncursor.execute(query)
            connection.commit()
        except mysql.connector.errors.IntegrityError:
            # Duplicate entry, ignore
            pass
    finally:
        connectioncursor.close()
        connection.close()

# Ercot Scraper
# @author Josh Braden
# Python script to download report files from Ercot and insert them into a MySQL database for Grafana dashboards

# Imports
import sys
import requests
import mysql.connector
from bs4 import BeautifulSoup

# Variables
version = "v0.0"
# Ercot stuff
baseUrl = "http://mis.ercot.com"
reportBaseUrl = "/misapp/GetReports.do?reportTypeId="
docBaseUrl = "/misdownload/servlets/mirDownload?mimic_duns=000000000&doclookupId=837782145"
# DB Stuff
dbhost = "127.0.0.1"
dbuser = "dbuser"
dbpasswd = "password"
dbschema = "ercot"
dbcompress = False
# These should be fine unless you also altered the schema file
dbcharset = "utf8mb4"
dbcollation = "utf8mb4_general_ci"
# Helptext
helptext = "Usage: ercotscraper.py foo"


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
        connectioncursor.execute("SELECT COUNT(*) FROM messageGrabs")
        connresult = connectioncursor.fetchone()
        for i in connresult:
            print("Success")

        connectioncursor.close()
        connection.close()
        return 0


# Function to get the list of available documents for a given report
def getDocs(reportId):
    url = baseUrl + reportBaseUrl + reportId
    req = requests.get(url)
    if req.status_code != 200:
        print("Error getting document list!")
        return -1

    soup = BeautifulSoup(req.content, "html.parser")
    # TODO soup parsing


# Execution start
print("Starting ercot scraper " + version)
if testMySQL() != 0:
    sys.exit(1)

if len(sys.argv) == 2:
    if sys.argv[1] == "help" or sys.argv[1] == "-h":
        # Print helptext
        print(helptext)

else:
    # Continue
    print("foo")

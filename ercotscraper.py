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
docBaseUrl = "/misdownload/servlets/mirDownload?mimic_duns=000000000&doclookupId="
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
        connectioncursor.execute("SELECT COUNT(*) FROM downloads")
        connresult = connectioncursor.fetchone()
        for i in connresult:
            print("Success")

        connectioncursor.close()
        connection.close()
        return 0


# Function to get the list of available documents for a given report
# Input: one report ID
# Output: List of documents on the server that haven't been downloaded
def getDocs(reportId):
    docUrls = []
    docIds = []
    url = baseUrl + reportBaseUrl + reportId
    req = requests.get(url)
    if req.status_code != 200:
        print("Error getting document list!")
        docUrls.clear()
        return docUrls

    soup = BeautifulSoup(req.content, "html.parser")
    # Build URL array
    for link in soup.find_all('a'):
        docUrls.append(link.get('href'))

    # Build ID array
    for url in docUrls:
        id = url.split("=")[-1]
        docIds.append(id)

    # Check if IDs exist in the database
    # First, set existing IDs to null
    for i in range(0, len(docIds)):
        # TODO import this function
        #if checkDbExistence(id, "downloads"):
        #    docIds[i] = 0
        print("Placeholder")

    # Then remove null values
    # From: https://www.delftstack.com/howto/python/python-list-remove-all/
    try:
        while True:
            docIds.remove(0)
    except ValueError:
        pass

    # Rebuild URL list with docs that need to be downloaded
    docUrls.clear()
    for id in docIds:
        url = baseUrl + docBaseUrl + str(id)
        docUrls.append(url)

    return docUrls


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

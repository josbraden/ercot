# Ercot Scraper
# @author Josh Braden
# Python script to download report files from Ercot and insert them into a MySQL database for Grafana dashboards

# Library imports
import csv
import io
import os
import requests
import sys
import datetime
import zipfile
from bs4 import BeautifulSoup
# File imports
from ercotmysql import testMySQL, checkDbExistence, addDownload, insertSolar

# Variables
version = "v0.1"
tempdir = "./tmp"
# Ercot stuff
baseUrl = "http://mis.ercot.com"
reportBaseUrl = "/misapp/GetReports.do?reportTypeId="
docBaseUrl = "/misdownload/servlets/mirDownload?mimic_duns=000000000&doclookupId="
# Helptext
helptext = "Usage: ercotscraper.py foo"


# Function to make sure required folders exist
def checkDir():
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)


# Function to get the list of available documents for a given report
# Input: one report ID
# Output: List of documents on the server that haven't been downloaded
def getDocList(reportId):
    docUrls = []
    docIds = []
    url = baseUrl + reportBaseUrl + str(reportId)
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
        if checkDbExistence(id, "downloads"):
            docIds[i] = 0

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


# Function to download data files from a docUrls array
# Input is the report ID and list of documents, outputs unzipped CSV files into the temp directory
# Additional output is download logs to the database
def downloadDocs(ercot_report_id, docUrls):
    for i in range(0, len(docUrls)):
        id = docUrls[i].split("=")[-1]
        req = requests.get(docUrls[i])
        if req.status_code != 200:
            addDownload(ercot_report_id, id, req.status_code)

        else:
            addDownload(ercot_report_id, id, req.status_code)
            # Discard XML files, unzip CSV files
            if "csv.zip" in req.headers['Content-Disposition']:
                print("Continue")
                z = zipfile.ZipFile(io.BytesIO(req.content))
                z.extractall(tempdir)


# Report function for solar
def report_solar():
    ercot_report_id = 13484
    docList = getDocList(ercot_report_id)
    if len(docList) == 0:
        return -1

    downloadDocs(ercot_report_id, docList)
    # Process downloaded CSVs
    for filename in os.listdir(tempdir):
        csvData = []
        fullFilename = tempdir + "/" + filename
        fp = open(fullFilename, "r")
        csvReader = csv.reader(fp, delimiter=',')
        # Read this file into RAM
        for row in csvReader:
            csvData.append(row)

        fp.close()
        for i in range(1, len(csvData)):
            queryData = ""
            sqlDateTime = datetime.datetime.strptime(csvData[i][0], '%m/%d/%Y %H:%M').strftime('%Y-%m-%d %H:%M:%S')
            queryData = str(csvData[i][1]) + ",'" + sqlDateTime + "'"
            insertSolar(queryData)

        os.remove(fullFilename)

    return 0


# Execution start
print("Starting ercot scraper " + version)
if testMySQL() != 0:
    sys.exit(1)

if len(sys.argv) == 2:
    if sys.argv[1] == "help" or sys.argv[1] == "-h":
        # Print helptext
        print(helptext)

else:
    # Startup checks
    checkDir()
    # Run through defined reports
    report_solar()

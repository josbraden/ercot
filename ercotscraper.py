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
from ercotconfig import tempdir

# Variables
version = "v0.1"
verbose = False
# Ercot stuff
baseUrl = "http://mis.ercot.com"
reportBaseUrl = "/misapp/GetReports.do?reportTypeId="
docBaseUrl = "/misdownload/servlets/mirDownload?mimic_duns=000000000&doclookupId="
# Helptext
helptext = "Usage: ercotscraper.py [-h|help] [-v]"


# Function to make sure required folders exist
def checkDir():
    if not os.path.exists(tempdir):
        os.makedirs(tempdir)


# Function to get the list of available documents for a given report
# Input: one report ID
# Output: List of documents on the server that haven't been downloaded
def getDocList(reportId):
    if verbose:
        print("Grabbing doc list...", end='')

    docUrls = []
    docIds = []
    url = baseUrl + reportBaseUrl + str(reportId)
    req = requests.get(url)
    if req.status_code != 200:
        if verbose:
            print("Error getting document list!")

        docUrls.clear()
        return docUrls

    if verbose:
        print("Success")

    soup = BeautifulSoup(req.content, "html.parser")
    # Build URL array
    for link in soup.find_all('a'):
        docUrls.append(link.get('href'))

    # Build ID array
    for url in docUrls:
        id = url.split("=")[-1]
        docIds.append(id)

    if verbose:
        print("Parsed " + str(len(docIds)) + " documents")

    # Check if IDs exist in the database
    # First, set existing IDs to null
    for i in range(0, len(docIds)):
        if checkDbExistence(docIds[i], "downloads"):
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

    if verbose:
        print(str(len(docUrls)) + " documents to download")

    return docUrls


# Function to download data files from a docUrls array
# Input is the report ID and list of documents, outputs unzipped CSV files into the temp directory
# Additional output is download logs to the database
def downloadDocs(ercot_report_id, docUrls):
    dlknt = 0
    extractknt = 0
    for i in range(0, len(docUrls)):
        id = docUrls[i].split("=")[-1]
        req = requests.get(docUrls[i])
        if req.status_code != 200:
            if verbose:
                print("Failed to download: " + str(id))

            addDownload(ercot_report_id, id, req.status_code)

        else:
            if verbose:
                print("Downloaded: " + str(id))

            addDownload(ercot_report_id, id, req.status_code)
            dlknt += 1
            # Discard XML files, unzip CSV files
            if "csv.zip" in req.headers['Content-Disposition']:
                print("Continue")
                z = zipfile.ZipFile(io.BytesIO(req.content))
                z.extractall(tempdir)
                extractknt += 1
                if verbose:
                    print("Extracted: " + str(id))

    if verbose:
        print("Downloaded " + str(dlknt) + " files")
        print("Extracted: " + str(extractknt) + " files")


# Report function for solar
def report_solar():
    ercot_report_id = 13484
    if verbose:
        print("Running solar")

    docList = getDocList(ercot_report_id)
    if len(docList) == 0:
        return -1

    downloadDocs(ercot_report_id, docList)
    # Process downloaded CSVs
    if verbose:
        print("Processing solar CSVs")

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

    if verbose:
        print("Finished solar")

    return 0


# Execution start
if len(sys.argv) == 2:
    if sys.argv[1] == "help" or sys.argv[1] == "-h":
        print(helptext)
        sys.exit(0)

    elif sys.argv[1] == "-v":
        verbose = True

if testMySQL() != 0:
    if verbose:
        print("Failed to connect to MySQL, check credentials")

    sys.exit(1)

else:
    if verbose:
        print("Successfully connected to MySQL")

if verbose:
    print("Starting ercot scraper " + version)

# Startup checks
checkDir()
# Run through defined reports
report_solar()

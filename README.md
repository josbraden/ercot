# Ercot

Python scripts to pull Ercot power reports and store them in MySQL, so they can be displayed in Grafana dashboards

## Requirements

Requirements to run this system

### Python

- python3
- python3-mysql.connector
- BeautifulSoup 4

In Debian based environments you can get all these through apt, and pip3 can also provide these libraries

### Database

Tested with Mariadb, should also work fine with MySQL

Included in the schema file is a stored procedure and disabled event to run data retention against the tables. Default values are to keep one month of downloaded documents, six months of solar and wind (since they get updated on 5-minute intervals), and one year for everything else.

### Other

Grafana, if you want to use the grafana dashboard

## Setup

1. Clone this repo
2. Create a database and import the schema from ercot.sql
3. Create a database user and password
4. Copy 'ercotconfig-example.py' to 'ercotconfig.py'
5. Enter config details in ercotconfig.py, should be pretty self explanatory
6. Execute the script to download and insert the data: `python3 ercotscraper.py`
7. To run on a schedule, set up a cron job. Examples in 'example.crontab'
8. (Optional) Set up grafana
  - Connect your MySQL database as a Grafana data source
  - Import and connect the grafana dashboard

## Misc Notes

The supply dataset seems a bit wonky. It only gets updated once and hour, as opposed to every fifteen minutes like 'demand' and doesn't seem to line up with the official dashboard exactly. I'm not sure if there's a better dataset to use.

The DC tie flow table has a composite key composed of the tie flow ID plus the datetime. This should be split into two tables, one for the tie flows and one for the flow data, but I don't feel like it.

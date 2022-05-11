# ercot

Systems to pull Ercot power reports and store them in MySQL, so they can be displayed in Grafana dashboards

## Requirements

Requirements to run this system

### Python

- python3
- python3-mysql.connector
- BeautifulSoup 4

### Database

Tested with Mariadb, should also work fine with MySQL

### Other

Grafana, if you want to use the grafana dashboard

## Setup

1. Clone this repo
2. Create a database and import the schema from ercot.sql
3. Create a database user and password
4. Copy 'ercotconfig-example.py' to 'ercotexample.py'
5. Enter config details in ercotexample.py, should be pretty self explanatory
6. Execute the script to download and insert the data: `python3 ercotscraper.py`
7. Import and connect the grafana dashboard

## Misc Notes

The supply dataset seems a bit wonky. It only gets updated once and hour, as opposed to every fifteen minutes like 'demand' and doesn't seem to line up with the official dashboard exactly. I'm not sure if there's a better dataset to use.

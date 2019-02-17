# Craigslist Paris Apartment Scrapper
The purpose of this application is to:
- Scape apartment listings from Craigslist Paris,
- Scrub and transform sq-m and number of bedrooms data,
- Write scrapped data into a SQL database, and
- Query and render data from SQL database in HTML using Flask.

# Process flow
![Design Pattern](exports/Scraper-Process-Flow.PNG)

# Dependencies
Refer to requirements.txt

# Getting Started
To run the CraigsListScraping application, run the bash script `run.sh`. 
It will start up a virtual environment, then launch the application which 
follows the process flow outlined above.
```
$ ./run.sh
```
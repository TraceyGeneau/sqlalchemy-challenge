# Module 10 SQLALCHEMY

## Decscription

A future trip is planned to Honolulu, Hawaii.  In order to get a better idea of the weather there, a climate analysis is recommended.  

## Part 1:  Analyze and Explore the Climate Data

### Precipitation Analysis

Two tables were used for this analysis.  The first was Hawaii measurements and it included the ID, station, date, precipitarion and temperature observed.  The second was Hawaii Station and it included the ID, station, name, tatitude, longitude and elevation. 

Given the dataset, the most recent recorded precipitation event was 2017-08-23 as determined from the measurement table.  From this date, a query was set up to determine the precipitation points for the last 12 months.  This is represented in the bar graph in figure 1.  

INSERT FIGURE

The summary statistics for this dat are:

count	2021
mean	0.177279
std	    0.461190
min	    0.000000
25%	    0.000000
50%	    0.020000
75%	    0.130000
max	    6.700000

### Exploratory Station Analysis

From the station analysis, it was determined there are a total of 9 weather stations in Hawaii with the most active being USC00519281 (2772 recoded measurements). The lowest temperature recorded at this sation was 54°F, the highest temperature recorded was 85°F and the average temperature of the station was 71.7°F.

The last recorded date found at this station was 2017-08-18.  The data from the 12 monthd prior to this date was recorded in histogram below (fig 2) indicating the highest frequency of measurements were taken at approximately 75°F to 77°F.

INSERT PICTURE

## Part 2: Design your Climat App

From the previous data, a Flask API was created.  The file with the coding for the app.py can be found in the Surf's Up folder of this repository.  The following were listed on the home route of the App:

Available Routes:
/api/v1.0/precipitation
/api/v1.0/stations
/api/v1.0/tobs

The dates in the following links can be altered in the web address.
The start or end date cannot be any later than 2017-08-23 and must be in theYYYY-MM-DD format

/api/v1.0/2016-08-23
/api/v1.0/2016-08-23/2017-08-23

For the Precipication Route, when selected, a list of all of the precipitation (prcp)measurments is derived dating from 2016-08-23 to 2017-08-23.

For the Stations Route, when selected, a list of the 9 stations appears with their station number. 

For the Tobs Route, a list of the total observed temperatures (tobs) for the most active station, USC00519281, from 2016-08-18 to 2017-08-18.

Also, if the user enters /api/v1/YYYY-MM-DD (no later than 2017-08-23) they will get the minimum, masimum and average temperature from that date until the last recorded date 2017-08-23.

Another neat feature is if the user enters /api/v1/YYYY-MM-DD/YYYY-MM-DD for a start and end date (no later than 2017-08-23) the minimum, maximum and average temperatures between the start date and end date will appear.





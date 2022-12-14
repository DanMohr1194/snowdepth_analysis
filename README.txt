PYTHON SNOW DEPTH ANALYZER

This project analyzes daily snow depth from 1999 to 2020 using data from the
Canadian Meteorological Center's Daily Snow Depth Analysis Data (NSIDC-0447)
https://nsidc.org/data/nsidc-0447/versions/1

INSTALLATION AND RUNNING

To install this, download the python files from github. From NSIDC,
download the ASCII files for each year you wish to analyze into the
same directory, along with cmc_analysis_ps_lat_lon_v01.2.txt.

Running 'snow_trendmaker.py' will output a plot of days of snow depth above a 
set threshold at a particular location with a rolling 3 year average,
along with a CSV of the same data. 

'snow plots year.py' outputs a plot of daily snow depth over the course of a
calendar year in a particular location.

Note that this only works for locations in the northern hemisphere.

'''
Trying to plot daily snow depth
over a year at a particular location
'''

import pandas as pd
from datetime import date
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#timing program, delete later
start_time = time.time()

#initial global variables
#the location, using Minocqua, WI here
loc_lat = 45.8711
loc_lon = -89.7093
loc_name = 'Minocqua, WI'
#year we want to plot
year = 2020

#converting the latitude and longitude, finding closest I and J
lat_lon_df = pd.read_fwf('cmc_analysis_ps_lat_lon_v01.2.txt', infer_nrows=100000, skiprows=(0,1,2,3,4,5,6,8))
lat_lon_df['Lat'] = (loc_lat-lat_lon_df['Lat']).abs()
lat_lon_df['Long'] = (loc_lon-lat_lon_df['Long']).abs()
lat_lon_df['Lat + Long'] = lat_lon_df['Lat'] + lat_lon_df['Long']
loc_idx = lat_lon_df['Lat + Long'].idxmin()
loc_i = lat_lon_df.loc[loc_idx, 'I']
loc_j = lat_lon_df.loc[loc_idx, 'J']

#creating a df for the depths to go into
daily_depth = pd.DataFrame()
jan1 = date(year,1,1)
dec31 = date(year,12,31)
day_list = [d.strftime('%d%b') for d in pd.date_range(start=jan1, end=dec31)]
daily_depth['Date'] = day_list
depth_list = []

#now actually reading the data and putting it into daily_depth
long_list = list(map(str,[n for n in range(1,707)]))
for chunk in pd.read_table(f'cmc_sdepth_dly_{str(year)}_v01.2.txt', names=long_list, dtype=str, delim_whitespace=True, 
                         header=None, engine='python', chunksize=707):
    chunk = chunk.reset_index(drop=True)
    depth = float(chunk.loc[loc_i, str(loc_j)])
    depth_list.append(depth)
    print(chunk.loc[0,'1'])
    print(depth)

#cleaning up the dates to be readable, adding rolling 7 day average
daily_depth['Depth']=depth_list
daily_depth['Rolling']=daily_depth['Depth'].rolling(7).mean()

#plotting this
locator = mdates.MonthLocator()  
fmt = mdates.DateFormatter('%b')
plt.xlabel('Date')
plt.ylabel('Snow Depth (cm)')
plt.grid()
plt.title(f'Daily Snow Depth in {str(year)} at {loc_name}')
plt.plot(day_list,depth_list,'ro')
plt.plot(day_list, daily_depth['Rolling'], label='7 day rolling mean')
X = plt.gca().xaxis
X.set_major_locator(locator)
X.set_major_formatter(fmt)
plt.legend()
plt.savefig(f'{loc_name}_{str(year)}.png', dpi=1200)
plt.show()
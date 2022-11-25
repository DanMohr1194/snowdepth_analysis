'''
creating a plot of number of yearly days
with snow above a particular depth at a
given location.
'''
import pandas as pd
from datetime import date, timedelta
import matplotlib.pyplot as plt
import numpy as np

#initial global variables
#the location, using Minocqua, WI here
loc_lat = 45.8711
loc_lon = -89.7093
loc_name = 'Minocqua, WI'
#the depth we want to count days above, in cm
depth_threshold = 15.0
#the time range (works from 1999 to 2020)
start_year = 1999
end_year = 2020

#creating lists for a df for the snowy days/year to go into
year_list = list(range(start_year, end_year+1))
snowday_list = []

#converting the latitude and longitude, finding closest I and J
lat_lon_df = pd.read_fwf('cmc_analysis_ps_lat_lon_v01.2.txt', infer_nrows=100000, skiprows=(0,1,2,3,4,5,6,8))
lat_lon_df['Lat'] = (loc_lat-lat_lon_df['Lat']).abs()
lat_lon_df['Long'] = (loc_lon-lat_lon_df['Long']).abs()
lat_lon_df['Lat + Long'] = lat_lon_df['Lat'] + lat_lon_df['Long']
loc_idx = lat_lon_df['Lat + Long'].idxmin()
loc_i = lat_lon_df.loc[loc_idx, 'I']
loc_j = lat_lon_df.loc[loc_idx, 'J']

#calculating the yearly snowy days
def snowday_count(year):
    filename = f'cmc_sdepth_dly_{str(year)}_v01.2.txt'
    #creating a df for the depths to go into
    daily_depth = pd.DataFrame()
    jan1 = date(year,1,1)
    dec31 = date(year,12,31)
    day_list = [d.strftime('%d%b') for d in pd.date_range(start=jan1, end=dec31)]
    daily_depth['Date'] = day_list
    depth_list = []
    #now actually reading the data and putting it into daily_depth
    #speeding things up/cleaner output w/ chunking
    long_list = list(map(str,[n for n in range(1,707)]))
    for chunk in pd.read_table(filename, names=long_list, dtype=str, delim_whitespace=True, 
                             header=None, engine='python', chunksize=707):
        chunk = chunk.reset_index(drop=True)
        depth = float(chunk.loc[loc_i, str(loc_j)])
        depth_list.append(depth)
        '''printing the date and depth to
        keep track of where I'm at while
        running'''
        print(chunk.loc[0,'1'])
        print(depth)
    daily_depth['Depth']=depth_list
    snowy_days=(daily_depth['Depth']>=depth_threshold).sum()
    return snowy_days

#running the above over each year and populating the count
for i in range(start_year, end_year+1):
    snowday_list.append(snowday_count(i))

#making a dataframe of snowy days per year w/rolling 3 year average
yearly_snowdays = pd.DataFrame()
yearly_snowdays['Year'] = year_list
yearly_snowdays['Days'] = snowday_list
yearly_snowdays['Rolling'] = yearly_snowdays['Days'].rolling(3).mean()

#testing
print(yearly_snowdays)

#outputting to CSV for future use
yearly_snowdays.to_csv(f'{loc_name}_{str(depth_threshold)}cm_{str(start_year)}_{str(end_year)}.csv')

#now plotting it
plt.xlabel('Year')
plt.ylabel('Days')
plt.grid()
plt.title(f'Days with over {str(depth_threshold)}cm of snow depth at {loc_name}')
plt.plot(year_list,snowday_list,'ro')
plt.plot(year_list, yearly_snowdays['Rolling'],label='3 year rolling mean')
plt.xticks(np.arange(min(year_list), max(year_list)+1, 2.0))
plt.legend()
plt.savefig(f'{loc_name}_{str(depth_threshold)}cm_{str(start_year)}_{str(end_year)}.png', dpi=1200)
plt.show()
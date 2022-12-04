'''
creating an output and map of average 
days per year with snow above a particular
depth across the northern hemisphere
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#initial global variables
#the depth we want to count days above, in cm
depth_threshold = 15.0
#the time range (works from 1999 to 2020)
start_year = 2018
end_year = 2020
year_counter = end_year-start_year+1
#empty array I'll append later with snowday_check
daycount_3D = np.empty((706,706))

#checking each coord for appropriate depth
def snowday_check(year):
    filename = f'cmc_sdepth_dly_{str(year)}_v01.2.txt'
    #now actually reading the data and putting it into np arrays
    yearcount = np.empty((706,706))
    long_list = list(map(str,[n for n in range(1,707)]))
    for chunk in pd.read_table(filename, names=long_list, dtype=float, delim_whitespace=True, 
                             header=None, engine='python', chunksize=707):
        chunk = chunk.reset_index(drop=True)
        print(chunk)
        chunk = chunk.drop([0]).reset_index(drop=True)
        np_chunk = chunk.to_numpy()
        bin_chunk = np.where(np_chunk >= depth_threshold, 1.0, 0.0) #gives 1 if depth is above threshold, 0 if below
        yearcount = np.dstack((yearcount, bin_chunk))
    return yearcount

#running the above function for each year, making daycount a 3D array
for i in range(start_year, end_year+1):
    daycount_3D = np.dstack((daycount_3D, snowday_check(i)))
    
#adding up daycount to be total days above threshold and making an average
daycount_total = np.sum(daycount_3D, axis=2)
daycount_avg = daycount_total/year_counter

#mapping the data
snowmap = plt.imshow(daycount_avg)
cbar = plt.colorbar()
cbar.set_label('Number of Days')
plt.title(f'Average days per year above {str(depth_threshold)}cm from {str(start_year)} to {str(end_year)}')
plt.axis('off')
plt.savefig(f'map_{str(depth_threshold)}cm_{str(start_year)}_{str(end_year)}.png', dpi=1200)
plt.show()
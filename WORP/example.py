import pandas as pd
from datetime import datetime, timedelta
import Data.getData as data
import Data.filterData as fltr
import Data.visualization.getHeatMap as hM
import Data.visualization.timeCourse as tC
import Data.visualization.timeSerie as tS
import Data.visualization.map as map


hours = 24
filter = 1
filterValue = 30

# create a Data obj
p1 = data.Data(
        "P1", # either P1 or P2
        filter=filter, filterValue=filterValue, # filter determines the type of filter("None", 1, 2); filterValue ist value for the filter
        timeframe=(datetime(2019, 12, 30), datetime(2019, 12, 30) + timedelta(hours=hours)) # timeframe
        #coordinates=([51,52], [9,10]) # coordinates
    )

p2 = data.Data("P2", filter, filterValue, timeframe=(datetime(2019, 12, 30), datetime(2019, 12, 30) + timedelta(hours=hours)))

# get the df from the data
df1 = p1.getData()
df2 = p2.getData()

# returns the time course from the sensor with the hight/lowest mean value
tC.timeCourseMaxMin(p1, df1)

# shows correlation between P1 and P2 values: is represented as heatmap
hM.buildHeatMap(df1, df2)

# shows time serie between P1 and P2
tS.timeSerie(df1, df2)

# plots the data on a map and saves it as "index.html"
map.showMap(p1, df1)

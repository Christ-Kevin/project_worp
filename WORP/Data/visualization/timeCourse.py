import pandas as pd
from datetime import datetime, timedelta, time
import matplotlib.pyplot as plt


def timeCourseMaxMin(dataObj, df):
    """plots the two sensors with the highst/lowest mean value"""

    name = dataObj.getPM() # either P1 or P2
    meanValue = df.groupby(["id"]).mean() # getting for every sensor the mean value

    # getting from meanValue the highst and lowest mean value
    max = meanValue.max()
    min = meanValue.min()

    # getting the sensorId from the max and min value
    for i in range(len(meanValue[name])):
        if meanValue[name][i] == max[name]:
            maxId = meanValue.index[i]
        if meanValue[name][i] == min[name]:
            minId = meanValue.index[i]


    # copies the df
    maxDf = df.copy()
    minDf = df.copy()

    # removing every element from the df except those from max/min sensor
    maxDf["id"] = df["id"][df["id"] == maxId]
    minDf["id"] = df["id"][df["id"] == minId]
    # drops the appering null values
    maxDf.dropna(subset = ["id"], inplace=True)
    minDf.dropna(subset = ["id"], inplace=True)

    # combines the two df into one concat df
    concatDf = pd.concat([maxDf, minDf])

    # plots through the new df
    concatDf.set_index("date", inplace=True)
    concatDf.groupby("id")[name].plot(legend=True) # plots for every sensor in concatDf
    plt.title("pollution for the highest/lowest mean from sensor")
    plt.xlabel("time in hours")
    plt.show()

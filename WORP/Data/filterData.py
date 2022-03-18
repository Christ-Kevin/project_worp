#Imports
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt


class Filter:
    """gets a df as input in the format:
        date  P1/P2  id longitude latitude
        df can be easily created with getData method
    """
    df = []
    max = 0 # max value from df after the filtering

    def __init__(self, data):
        """constructor"""
        self.df = data # pd in format as above

    def filterData(self, name, method, value):
        """filters the pd and plts max pollution and prints the highst value
                name: is the column name from the data(P1/P2),
                method: indicates which filter is used,
                value: ist the value for the filter (either float/int or a tuple with float/int)
        """

        self.filterNull(name) # filters all values under 0 (including 0)

        if method == 1:
            self.limit(name, value) # limit() sets a limit
        elif method == 2:
            self.quantile(name, value) # quantile() sets quantile

        self.printMaxPollution(name) # prints the max value (and when/where)
        self.plotMean(name) # plots the mean value during every hour
        return self.df


######################## filter methods ##############################

    def filterNull(self, name):
        """filters all 0 or lower values"""
        self.df[name] = self.df[name][self.df[name] > 0]

    def limit(self, name, value):
        """sets a max or min and max value for the data"""
        if str(type(value)) == "<class 'int'>":
            self.df[name] = self.df[name][self.df[name] < value] # removes every value larger than "value"

        if str(type(value)) == "<class 'tuple'>":
            self.df[name] = self.df[name][self.df[name] > value[0]] # removes every value smaller than "value"
            self.df[name] = self.df[name][self.df[name] < value[1]] # removes every value smaller than "value"
        self.df.dropna(subset = [name], inplace=True) # drops the rows with the upcoming NaN values

    def quantile(self, name, value):
        """returns all values below or in between the quantile/s"""
        if str(type(value)) == "<class 'float'>":

            # gets the quantile from the df
            q = self.df[name].quantile(value)

            # removes all elments not in the quantile
            self.df[name] = self.df[name][self.df[name] < q]

        elif str(type(value)) == "<class 'tuple'>":

            # gets the two quantiles from the df
            q1 = self.df[name].quantile(value[0])
            q2 = self.df[name].quantile(value[1])

            # removes elements not between the quantiles
            self.df[name] = self.df[name][self.df[name] > q1]
            self.df[name] = self.df[name][self.df[name] < q2]

        self.df.dropna(subset = [name], inplace=True) # drops the rows with the upcoming NaN values


    def printMaxPollution(self, name):
        """determines the max value of the df und prints it stats"""
        self.max = self.df[name].max()
        print("maxPollution: ")
        max = self.df.max()
        print("Value: " + str(max[1]))
        print("date: " + str(max[0]))
        print("longitude: " + str(max[3]))
        print("latitude: " + str(max[4]))

    def plotMean(self, name):
        """plots the mean value for every hour for the filtered data"""
        data = self.df.copy() # copys the df
        data["date"] = data["date"].dt.hour # overwrites the datetime with just the hour

        meanValues = data.groupby(["date"]).mean() # creates a pd with just the meanValues from every hour

        # plots the pd with matplotlib
        meanValues[name].plot()
        plt.title("mean pollution")
        plt.xlabel("time in hours")
        plt.ylabel(name)
        plt.show()

######################## setter and getter ###########################

    def getMaxValue(self):
        """get maxValue from the filtered data"""
        return self.max

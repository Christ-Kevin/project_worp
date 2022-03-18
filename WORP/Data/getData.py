## Rest Call to Luftdaten API
# https://documenter.getpostman.com/view/9745663/SWLmWPKX?version=latest#db5fdd76-e1c5-4ae1- 85d6-148666c7867e
# The API currently has a time limit of max 24hours time range per request.

# Imports
import requests
from .filterData import Filter
from datetime import datetime, timedelta
import pandas as pd

class Data:

    # Basic parameters
    base_url='http://sensordata.gwdg.de/api/' # Select Endpoint (P1 or P2)
    pm = "P1"

    # Select geo-coordinates (values are just examples ..)
    latrange=[51,52]
    longrange=[9,10]
    coordinates = (latrange, longrange)

    # Select time range (values are just examples ..)
    start_date = datetime(2018, 12, 30)
    end_date = (start_date + timedelta(hours=1))
    timeframe = (start_date, end_date)

    # Build the query
    mydata = '{"timeStart": "'+start_date.strftime("%Y-%m-%dT%H:%M:%SZ")+'",' + \
            '"timeEnd": "'+end_date.strftime("%Y-%m-%dT%H:%M:%SZ")+'", "area":  \
            {"coordinates":['+str(latrange)+','+str(longrange)+']}}'

    filter = "None"
    filterValue = 0
    filterObj = 0


    def __init__(self, pm="P1", filter="None", filterValue=0, timeframe=(datetime(2019, 12, 30), datetime(2019, 12, 30) + timedelta(hours=1)), coordinates=([51,52], [9,10])):
        """constructor
                pm: is the type of the data (usually P1/P2)
                filter: is either "None" or 0, if you don't want a filter or 1 for a limit or 2 for quantiles
                filterValue: is the value for the applied filter either an int/float or a tuple with two ints/floats
                timefram: is the period from where you get the data; Format is a tuple with two datetimes; Max difference are 24 hours
                coordinates: is the place from where you take the data; its a tuple with an longitude and latitude vector
        """

        self.pm = pm # either PM1 or PM2
        self.start_date = timeframe[0] # begin of the timeframe
        self.end_date = timeframe[1] # end of the timeframe
        self.latrange = coordinates[0] # latitude
        self.longrange = coordinates[1] # Longitude
        self.filter = filter # type of filter either "None"/0 or 1 or 2
        self.filterValue = filterValue # the value that you'r using for the filter

    def getData(self):
        """executes all methodes to transform and filter the data into a pd"""
        data = self.runQuery(self.buildQuery()) # get data
        data = self.transformPD(data) # transform into pd
        if not (self.filter == "None" or self.filter == 0): # filter data
            if (self.filter < 0) or (self.filter > 2):
                raise ValueError("Filter must be an int between 0 and 2 or 'None'!") # if input is not matching
            data = self.changeFilter(data, self.filter, self.filterValue)
        return data

    def changeFilter(self, data, filter, value):
        """changing the filter
            data: is the name of the column with the data
            filter: is the typ of filter(0, 1, 2)
            value: is the value for the applied filter
        """

        self.filter = filter # setting filter in case that it's getting changes manually
        newFilter = Filter(data) # creating filter object
        self.filterObj = newFilter # in case you wanna acces the filter object to get additional values
        newData = newFilter.filterData(self.pm, filter, value) # applying the filter
        return newData

    def buildQuery(self):
        """rebuilding the query"""

        mydata = '{"timeStart": "'+self.start_date.strftime("%Y-%m-%dT%H:%M:%SZ")+'",' + \
                '"timeEnd": "'+self.end_date.strftime("%Y-%m-%dT%H:%M:%SZ")+'", "area":  \
                {"coordinates":['+str(self.latrange)+','+str(self.longrange)+']}}'
        return mydata

    def runQuery(self, query, show="False"):
        """run the query"""
        response = requests.post(self.base_url + "measurements/" + self.pm,data=query)

        if show == True: # in case you wanna see the raw data
            print(query)
            print(response.text)

        return response.text

########################### transfrom into pd ####################################

    def transformPD(self, data):
        """transforms the data-list into a pandas-dataframe"""
        arr1d = data.strip('["time","lat","lon",' + self.pm + ',"sensor_id"],"sensor",[').split('],[')    # remove the header from the string
                                                                                              # split String into elements of a list
        arr1d[0] = '"' + arr1d[0]                            # add quotation mark at the first position of the first element of the list
        arr1d[-1] = arr1d[-1] + '"'                          # add quotation mark at the last position of the last element of list

        arr2d = []                         # adding a secound dim
        for i in arr1d:
            arr2d.append(i.split(","))   # spliting the Strings of the list  into another list

        # cleanses the different columns from the raw data and puts it a new list
        cleansed_date = self.cleanse_dates(arr2d)
        cleansed_data = self.cleanse_values(arr2d, 3)
        cleansed_sensorid = self.cleanse_values(arr2d, 4)
        for i in cleansed_sensorid:
            i.replace('\"', '')
        converted_longitude = self.cleanse_values(arr2d, 1)
        converted_latitude = self.cleanse_values(arr2d, 2)

        df = pd.DataFrame({"date":cleansed_date,self.pm:cleansed_data, "id":cleansed_sensorid, "longitude": converted_longitude, "latitude": converted_latitude}) # {"date":date, "P1":dataP1, "P2":dataP2}
        df[self.pm] = df[self.pm].str.replace('null','0')
        df = df.astype({self.pm: float, "longitude": float, "latitude": float})
        return df

    def cleanse_dates(self, arr2d):
        """cleanses the date-elment and convertes it into a date Typ"""
        date=[]
        for i in range(len(arr2d)): # removes unfitting elements
            arr2d[i][0] = arr2d[i][0].replace('T', ' ')
            arr2d[i][0] = arr2d[i][0].replace('Z', '')
            arr2d[i][0] = arr2d[i][0].replace('\"', '')

            if not len(arr2d[i][0]) == 19: # eliminates corrupted data, through a length check
                arr2d[i][0] = "2000-01-01 00:00:00"
            arr2d[i][0] = datetime.strptime(arr2d[i][0], "%Y-%m-%d %H:%M:%S") # converting into date type
            date.append(arr2d[i][0])
        return date

    def cleanse_values(self, arr2d, index):
        """restructures the values"""
        data=[]
        for i in range(len(arr2d)):
            data.append(arr2d[i][index])
        return data

########################### setter and getter ####################################

    def setPM(self, pm):
        """set either PM1 or PM2"""
        self.pm = pm

    def getPM(self):
        """get PM-Value"""
        return self.pm

    def setCoords(self, latrange, longrange):
        """set coordinates"""
        self.latrange = latrange
        self.longrange = longrange

    def getCoords(self):
        """get coordinates"""
        return (self.latrange, self.longrange)

    def setTimeframe(self, start_date, end_date):
        """set timeframe"""
        self.start_date = start_date
        self.end_date = end_date

    def getTimeframe(self):
        """get timeframe"""
        return (self.start_date, self.end_date)

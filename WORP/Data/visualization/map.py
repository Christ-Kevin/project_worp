import folium
import pandas as pd
import branca.colormap
from collections import defaultdict

def showMap(dataObj, df):
    """creates and saves a map as html for every sensor(mean value) in the df"""

    # start coordinates
    longitude = (dataObj.getCoords()[0][0] + dataObj.getCoords()[0][1])/2
    latitude = (dataObj.getCoords()[1][0] + dataObj.getCoords()[1][1])/2

    # creates the map
    m = folium.Map(location=[longitude, latitude], zoom_start=10)

    # grouping by id and calculating the mean value for each sensor
    meanValues = df.groupby(["id"]).mean()

    # creates legend for the map
    steps=10 # amount of "colorsteps"
    colormap = branca.colormap.linear.YlOrRd_09.scale(0, 25).to_step(steps) # legend is between 0 and 25
    
    colormap.add_to(m) # Add color bar at the top of the map

    # adding each sensor as a circle
    for i, k, j in zip(meanValues["longitude"], meanValues["latitude"], meanValues["P1"]):
        folium.Circle(
            legend_name="legend",
            radius=1500, # radius of circle
            color="#404040", # color of circle-border
            location=[i, k], # longitude latitude
            popup="long:" + str(round(i, 4)) + " lat:" + str(round(k, 4)), # click in cirlce to get coords
            tooltip=round(j, 4), # hover over circle to show value
            fill=True,
            fill_color=getColor(j), # color type depends on value
            fill_opacity=0.6 # color strength
        ).add_to(m)

    # shows coordinates on map
    m.add_child(folium.LatLngPopup())

    # saves the map as html
    m.save("index.html")

def getColor(value):
    """returns Hex_color depending on the size of Value"""
    gradient = { # diiferent colors as dict
        2.5: '#FCFCD0', #white
        5: '#FCF0AF',
        7.5: '#FAE392',
        10: '#F0C46C', # orange
        12.5: '#FCAC5D',
        15: '#FB844E',
        17.5: '#F0583D', #red
        20: '#DE363C',
        22.5: '#BF2842',
        25: '#8E283F'
    } # dark red

    for k, i in gradient.items():
        if value < k:
            return i # returns the color
    return "#8E283F" # if value is larger than 25

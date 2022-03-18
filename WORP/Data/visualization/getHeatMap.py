# Imports
import pandas as pd
import numpy as np
import seaborn as sn
import matplotlib.pyplot as plt

# buildHeatMap takes two objects('P1' and 'P2') as arguments,
# merged the obtained dataframes(2) into one dataframe with mergeDF()
# delete null values with the functin dropna()
# calculate and return the correlation coefficient between 'P1' and 'P2'  with np.corrcoef()
# show the heatMap
def buildHeatMap(df_P1, df_P2, plot=True):

    df = mergeDF(df_P1, df_P2)  # two dataframes with 'P1'(df1)- and 'P2'-values(df2) are merged into one dataframe df 

    # delete lines with null-values
    df = df.dropna(how='any',axis=0)

    # correlation coefficient between 'P1' and 'P2'
    # calculate pearson coefficient with numpy
    a=np.corrcoef(df["P1"],df["P2"])

    x_axis_labels = ["P1", "P2"]                  # labels for x-axis
    y_axis_labels = ["P1", "P2"]                  # labels for y-axis

    # create heatmap with seaborn
    sn.heatmap(a, annot=True, cmap='coolwarm',  xticklabels=x_axis_labels, yticklabels=y_axis_labels)

    plt.title('Correlation matrix P1/P2', fontsize = 17) # title with fontsize 17
    plt.xlabel('P-Values', fontsize = 12)         # x-axis label with fontsize 12
    plt.ylabel('P-Values', fontsize = 12)         # y-axis label with fontsize 12

    # show Heatmap
    if plot == True:
        plt.show()

    # return correlation matrix
    return a

# mergeDF merge 2 dataframes into one dataframe and returns it
def mergeDF(df_P1, df_P2):
    df = df_P1.merge(df_P2, how='left', left_on=['id', 'date'], right_on=['id', 'date'])   # merged dataframe has now 3 columns
    # returns the merged dataframe
    return df

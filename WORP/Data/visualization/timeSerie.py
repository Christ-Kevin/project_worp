#Imports
import matplotlib.pyplot as plt
import project_worp.WORP.Data.visualization.getHeatMap as gHM

# timeSerie takes 2 Dataframes as arguments
# convert the Dataframes into one Dataframe with gHM.mergeDF
# change the format of date to the Stringformat '%H:%M
# plot a timeserie with the values of 'P1' and 'P2'

def timeSerie(df_P1, df_P2):

    # merge dataframes df_P1 and df_P2
    newDF = gHM.mergeDF(df_P1, df_P2)                  # df_P1 and df_P2 refer to the Data objects of 'P1'- and 'P2'-values                                                                          # df_P1 and df_P2 also contain values that refers to the date of registration
    
    newDF.dropna()
    # the format of the column 'date' of the new dataframe is modify
    newDF['date']=newDF['date'].apply(lambda x: x.strftime('%H:%M'))
    newDF.plot(x="date", y=["P1", "P2"], kind="line")                                # plot. "date" is for the x-axis and ["P1", "P2"] for the y-axis
    plt.ylabel("P-Values")                                              # y-label
    plt.title('Timeseries for P1- and P2-Values')                       # title
    plt.show()                                                          # show

    # return HeatMap and correlation matrix between dataObj1('P1') and dataObj2('P2')
    return gHM.buildHeatMap(df_P1, df_P2, False)

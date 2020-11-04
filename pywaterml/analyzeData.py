import pandas as pd
import numpy as np

class WaterAnalityca():
    """
        Get the mean interpolation of the values for an specific site
        MeanInterpolation() function is a complement to the
        GetValues() WaterML function if there is gaps in the data
    """
    def MeanInterpolation(GetValuesResponse):
        time_pd, values_pd = zip(*GetValuesResponse)
        pds={}
        pds['time'] = time_pd
        pds['value'] = values_pd
        df_interpolation= pd.DataFrame(pds,columns = ["time","value"])
        df_interpolation2= pd.DataFrame(pds,columns = ["time","value"])
        df_interpolation.loc[df_interpolation.value < 0] = np.NaN
        df_interpolation.replace(0, np.NaN, inplace=True)
        df_interpolation['time'] = pd.to_datetime(df_interpolation['time'])
        df_interpolation = df_interpolation.set_index('time').resample('D').mean()
        df_interpolation['value'] = df_interpolation['value'].interpolate()
        df_interpolation.reset_index(level=0, inplace=True)
        df_interpolation.replace(np.NaN,0, inplace=True)
        listVals = df_interpolation['value'].to_list()
        listTimes = df_interpolation['time'].to_list()
        dataInterpolated = []
        #a count for the number of interpolated can be introduced
        for t,v in zip(listTimes,listVals):
            dataInterpolated.append([t,v])

        return dataInterpolated
    
if __name__ == "__main__":
    print("Why are you running the wrapper class file?")

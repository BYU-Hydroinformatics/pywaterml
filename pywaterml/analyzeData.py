import pandas as pd
import numpy as np

class WaterAnalityca():
    """
    This class represents the Analitics object for the WaterMLOperations class. The WaterAnalityca provides functions related to statistics(monthly and daily averages) and
    basic Math functionality(Interpolation). However, this is a helper class for the main WaterMLOperations class.
    """
    def _Interpolate(GetValuesResponse, type='mean'):
        """
        Helper function to rerieve different kinds of interpolation in the WaterMLOperations GetInterpolation() function
        Args:
            GetValuesResponse: GetValues Response from WaterMLOperations GetValues() function
            type: Type of interpolation
        Returns:
            dataInterpolated: Interpolated data
        """
        time_pd, values_pd = zip(*GetValuesResponse)
        pds={}
        pds['time'] = time_pd
        pds['value'] = values_pd
        df_interpolation= pd.DataFrame(pds,columns = ["time","value"])
        df_interpolation2= pd.DataFrame(pds,columns = ["time","value"])
        df_interpolation.loc[df_interpolation.value < 0] = np.NaN
        df_interpolation.replace(0, np.NaN, inplace=True)
        df_interpolation['time'] = pd.to_datetime(df_interpolation['time'])

        if type == 'mean':
            df_interpolation = df_interpolation.set_index('time').resample('D').mean()

        if type == 'backward':
            df_interpolation = df_interpolation.set_index('time').resample('D').bfill()

        if type == 'forward':
            df_interpolation = df_interpolation.set_index('time').resample('D').pad()

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

    def _MonthlyAverages(GetValuesResponse):
        """
        Helper function to rerieve the monthly averages from the WaterMLOperations GetValues() function in the GetMonthlyAverage() function
        Args:
            GetValuesResponse: GetValues Response from WaterMLOperations GetValues() function
        Returns:
            m_avg: monthly_average array
        """
        columns = ['dates','values']
        df = pd.DataFrame(GetValuesResponse['values'], columns=columns)
        df['dates'] = pd.to_datetime(df['dates'])
        df_2 = df.groupby(df.dates.dt.strftime('%m')).values.agg(['mean'])
        # df_2 = df.groupby(df.dates.dt.strftime('%Y-%m')).values.agg(['mean'])
        # print(df_2)
        m_avg = df_2.to_numpy()
        m_avg = m_avg.reshape((m_avg.shape[0],))
        m_avg = m_avg.tolist()
        return m_avg

    def _DailyAverages(GetValuesResponse):
        """
        Helper function to rerieve the daily averages from the WaterMLOperations GetValues() function in the GetDailyAverage() function
        Args:
            GetValuesResponse: GetValues Response from WaterMLOperations GetValues() function
        Returns:
            d_avg: daily_average array
        """
        d_avg = []
        return d_avg


if __name__ == "__main__":
    print("Why are you running the wrapper class file?")

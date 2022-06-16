import pandas as pd
import numpy as np
import logging
class WaterAnalityca():
    """
    This class represents the Analitics object for the WaterMLOperations class. The WaterAnalityca provides functions related to statistics(monthly and daily averages) and
    basic Math functionality(Interpolation). However, this is a helper class for the main WaterMLOperations class.
    """
    def _Interpolate(GetValuesResponse, type='mean', timeUTC = False):
        """
        Helper function to rerieve different kinds of interpolation in the WaterMLOperations GetInterpolation() function
        Args:
            GetValuesResponse: GetValues Response from WaterMLOperations GetValues() function
            type: Type of interpolation
        Returns:
            dataInterpolated: Interpolated data
        """
        try:
            return_array = GetValuesResponse['values']
            df = pd.DataFrame.from_dict(return_array)
            pds={}
            if timeUTC is True:
                pds['time'] = df['dateTimeUTC'].tolist()
            else:
                pds['time'] = df['dateTime'].tolist()
            pds['value'] = df['dataValue'].tolist()
            df_interpolation= pd.DataFrame(pds,columns = ["time","value"])
            print(df_interpolation)
            df_interpolation.replace("No Data Provided", np.NaN, inplace=True)
            df_interpolation.loc[df_interpolation.value < 0] = np.NaN
            # df_interpolation.replace(0, np.NaN, inplace=True)
            df_interpolation['time'] = pd.to_datetime(df_interpolation['time'])

            if type == 'mean':
                df_interpolation = df_interpolation.set_index('time').resample('D').mean()

            if type == 'backward':
                df_interpolation = df_interpolation.set_index('time').resample('D').bfill()

            if type == 'forward':
                df_interpolation = df_interpolation.set_index('time').resample('D').pad()

            df_interpolation['value'] = df_interpolation['value'].interpolate()
            df_interpolation.reset_index(level=0, inplace=True)
            # df_interpolation.replace(np.NaN,0, inplace=True)
            listVals = df_interpolation['value'].to_list()
            listTimes = df_interpolation['time'].to_list()
            dataInterpolated = []
            for t,v in zip(listTimes,listVals):
                dataInterpolated.append([t,v])
        
            return dataInterpolated

        except Exception:
            logging.error("No possible to interpolate",exc_info=True)
            dataInterpolated = []
            return dataInterpolated

    def _MonthlyAverages(GetValuesResponse):
        """
        Helper function to rerieve the monthly averages from the WaterMLOperations GetValues() function in the GetMonthlyAverage() function
        Args:
            GetValuesResponse: GetValues Response from WaterMLOperations GetValues() function
        Returns:
            m_avg: monthly_average array
        """
        try:
            return_array = GetValuesResponse['values']
            df_in = pd.DataFrame.from_dict(return_array)
            # time_pd, values_pd = zip(*GetValuesResponse)
            pds={}
            pds['dates'] = df_in['dateTime'].tolist()
            pds['values'] = df_in['dataValue'].tolist()
            columns = ['dates','values']
            df= pd.DataFrame(pds,columns = columns)
            df.replace("No Data Provided", np.NaN, inplace=True)
            # df = pd.DataFrame(GetValuesResponse['values'], columns=columns)
            df['dates'] = pd.to_datetime(df['dates'])
            df_2 = df.groupby(df.dates.dt.strftime('%m')).values.agg(['mean'])
            m_avg = df_2.to_numpy()
            m_avg = m_avg.reshape((m_avg.shape[0],))
            m_avg = m_avg.tolist()
            return m_avg

        except Exception:
            logging.error("No possible to give monthly averages",exc_info=True)
            m_avg = []
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

import pandas as pd
import numpy as np

class WaterAnalityca():
    """
        Get the mean interpolation of the values for an specific site
        MeanInterpolation() function is a complement to the
        GetValues() WaterML function if there is gaps in the data
    """
    def Interpolate(GetValuesResponse, type='mean'):
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

    def MonthlyAverages(GetValuesResponse):
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

    def dailyAverages(variable_site,CookieCutter = None):
        d_avg = []
        return d_avg

    def MonthlyAverageClusters(Sites, Variable):
        timeseries = []
        i = 0
        for site in Sites:
            print(i)
            site_full_code = f'{site["network"]}:{site["sitecode"]}'
            siteInfo =  water.GetSiteInfo(site_full_code)
            for sinfo in siteInfo:
                if sinfo['name'] == Variable:
                    print(site['name'])
                    firstVariableCode = siteInfo[0]['code']
                    variable_full_code = network + ":" + firstVariableCode
                    methodID = siteInfo[0]['methodID']
                    start_date = siteInfo[0]['timeInterval']['beginDateTime'].split('T')[0]
                    end_date = siteInfo[0]['timeInterval']['endDateTime'].split('T')[0]
                    variableResponse = water.GetValues(site_full_code, variable_full_code, methodID, start_date, end_date)
                    m_avg = water.getMonthlyAverage(variableResponse)
                    timeseries.append(to_time_series(m_avg))
                    break
            i = i + 1    
        # X = np.array(np.array(list2))
        formatted_time_series = to_time_series_dataset(timeseries)
        # print(X)
        model = TimeSeriesKMeans(n_clusters=2, metric="dtw", max_iter=10)
        y_pred = model.fit_predict(formatted_time_series)
        return y_pred

if __name__ == "__main__":
    print("Why are you running the wrapper class file?")

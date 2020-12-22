# from pywaterml.waterML import WaterMLOperations

# import sys
# sys.path.append("/home/elkin/Projects/condaPackages/pywaterml")
from pywaterml.waterML import WaterMLOperations
from tslearn.metrics import dtw
from tslearn.clustering import TimeSeriesKMeans
from tslearn.utils import to_time_series, to_time_series_dataset
import pandas as pd
import numpy as np
import time
url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
water = WaterMLOperations(url = url_testing)

def main():
    sites = water.GetSites()
    variables = water.GetVariables()
    print("************SITES***************")
    print(len(sites))
    print("************VARIABLES***********")
    print(variables)
    print("***********GET SITE INFO****************")
    site_full_code = "Para_La_Naturaleza:Rio_Toro_Negro"
    siteInfo =  water.GetSiteInfo(site_full_code)
    print(siteInfo)
    print("VALUES")
    network = sites[0]['network']
    firstVariableCode = siteInfo[0]['code']
    variable_full_code = network + ":" + firstVariableCode
    methodID = siteInfo[0]['methodID']
    start_date = siteInfo[0]['timeInterval']['beginDateTime'].split('T')[0]
    end_date = siteInfo[0]['timeInterval']['endDateTime'].split('T')[0]
    variableResponse = water.GetValues(site_full_code, variable_full_code, methodID, start_date, end_date)
    print("INTERPOLATION")
    interpol_b = water.GetInterpolation(variableResponse['values'], 'backward')
    interpol_f = water.GetInterpolation(variableResponse['values'], 'forward')
    interpol_m = water.GetInterpolation(variableResponse['values'], 'mean')
    print(len(interpol_f))
    print(len(interpol_b))
    print(len(interpol_m))

    m_avg = water.GetMonthlyAverage(None, site_full_code, variable_full_code, methodID, start_date, end_date)
    print(m_avg)
    y_pred = water.GetClustersMonthlyAvg(sites,siteInfo[0]['name'])
    print(len(y_pred))
    """
    UNCOMMENT TO USE WITH THE epsg:3857
    """
    # BoundsRearranged = [-7398417.229789019,2048546.619479188,-7368453.914701229,2080306.2047316788]
    # BoundsRearranged = [-7401666.338691997, 2060618.8113541743, -7378996.124391947, 2071003.588530944]
    # SitesByBoundingBox = water.GetSitesByBoxObject(BoundsRearranged,'epsg:3857')
    """
    UNCOMMENT TO USE WITH THE epsg:4326
    """
    BoundsRearranged = [-66.4903,18.19699,-66.28665,18.28559]
    SitesByBoundingBox = water.GetSitesByBoxObject(BoundsRearranged,'epsg:4326')
    print(len(SitesByBoundingBox))

    print("***********FILTERING SITES BY KEYWORD****************")
    variablesTest = [variables[0]]

    """
    USING A COOKIE CUTTER
    """
    sitesFiltered = water.GetSitesByVariable(variablesTest,sites)
    print("GetSitesByVariable With CookieCutter")
    print(len(sitesFiltered))

    """
    WITHOUT USING A COOKIE CUTTER
    """
    sitesFiltered = water.GetSitesByVariable(variablesTest)
    print("GetSitesByVariable No CookieCutter")
    print(len(sitesFiltered))

    print("******************CHANGE URL***********")
    water.ChangeEndpoint("http://hydroportal.cuahsi.org/CALVIN_HHS/cuahsi_1_1.asmx?WSDL")
    sites = water.GetSites()
    variables = water.GetVariables()
    print("************SITES***************")
    print(len(sites))
    print("************VARIABLES***********")
    print(variables)
    print("***********FILTERING SITES BY KEYWORD****************")
    variablesTest = [variables[0]]
    """
    USING A COOKIE CUTTER
    """
    sitesFiltered = water.GetSitesByVariable(variablesTest,sites)
    print("GetSitesByVariable With CookieCutter")
    print(len(sitesFiltered))
    """
    WITHOUT USING A COOKIE CUTTER
    """
    sitesFiltered = water.GetSitesByVariable(variablesTest)
    print("GetSitesByVariable No CookieCutter")
    print(len(sitesFiltered))
    columns = ['dates','values']
    df = pd.DataFrame(variableResponse['values'], columns=columns)
    # print(df.head())
    df['dates'] = pd.to_datetime(df['dates'])
    df_2 = df.groupby(df.dates.dt.strftime('%m')).values.agg(['mean'])
    # df_2 = df.groupby(df.dates.dt.strftime('%Y-%m')).values.agg(['mean'])
    # print(df_2)
    m_avg = df_2.to_numpy()
    m_avg = m_avg.reshape((m_avg.shape[0],))
    print(len(m_avg))
    start_time = time.time()
    y_pred = water.GetClustersMonthlyAvg(sitesFiltered,variablesTest[0])
    print(len(y_pred))
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Test was sucessful")

if __name__ == "__main__":
    main()

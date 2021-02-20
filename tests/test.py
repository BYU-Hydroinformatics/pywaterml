# from pywaterml.waterML import WaterMLOperations

import sys
sys.path.append("/home/elkin/Projects/condaPackages/pywaterml")
from pywaterml.waterML import WaterMLOperations
from tslearn.metrics import dtw
from tslearn.clustering import TimeSeriesKMeans
from tslearn.utils import to_time_series, to_time_series_dataset
import pandas as pd
import numpy as np
import time

url_testing = [
    # ["http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-country/hiscentral.asmx/GetWaterOneFlowServiceInfo",True],
    # ["http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-transboundary/hiscentral.asmx/GetWaterOneFlowServiceInfo",True],
    ["http://hydroportal.cuahsi.org/nevados/cuahsi_1_1.asmx?WSDL", False],
    ["http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL", False],
    ["http://hydroportal.cuahsi.org/CALVIN_HHS/cuahsi_1_1.asmx?WSDL", False],
    ["http://hydroportal.cuahsi.org/CCBEPDAP/cuahsi_1_1.asmx?WSDL", False],
    ["http://hydroportal.cuahsi.org/glacialridge/cuahsi_1_1.asmx?WSDL", False],
    ["http://hydroportal.cuahsi.org/KentState/cuahsi_1_1.asmx?WSDL", False],
    ["http://hydroportal.cuahsi.org/czo_boulder/cuahsi_1_1.asmx?WSDL", False],
    ["http://128.187.106.131/app/index.php/dr/services/cuahsi_1_1.asmx?WSDL", False],
    ["http://hydroportal.cuahsi.org/Ramsar_atacama/cuahsi_1_1.asmx?WSDL", False],
    ["http://hydrolite.ddns.net/italia/hsl-bol/index.php/default/services/cuahsi_1_1.asmx?WSDL", False],
    ["http://hydroportal.cuahsi.org/czo_catalina/cuahsi_1_1.asmx?WSDL", False],
    ["http://hydroportal.cuahsi.org/czo_catalina/cuahsi_1_1.asmx?WSDL", False],
    ["http://gs-service-production.geodab.eu/gs-service/services/essi/view/gs-view-and(whos-country,gs-view-country(RUS))/cuahsi_1_1.asmx?WSDL", False],
    ["http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-arctic/cuahsi_1_1.asmx?WSDL", False],
    ["http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-plata/cuahsi_1_1.asmx?WSDL", False]
]

# url_testing = "http://hydroportal.cuahsi.org/czo_catalina/cuahsi_1_1.asmx?WSDL"
# water = WaterMLOperations(url = url_testing)

def main():
    try:
        for url in url_testing:
            print("TESTING ", url)
            single_test_quick(url[0],url[1])
        print("Successful testing the different Endpoints")
    except Exception as e:
        print(e)


def single_test_quick(url_testing,url_catalog_testing = False):
    start_time = time.time()
    try:
        if url_catalog_testing:
            print("***************WOF GetWaterOneFlowServicesInfo****************")
            water = WaterMLOperations(url = url_testing)
            wateroneflowservices = water.GetWaterOneFlowServicesInfo()
            print("WaterOneFlow Services Available",wateroneflowservices)

            print("*************WOF Available and Not available******************")
            available_wof = water.AvailableServices()
            # print(available_wof)
            good_services = available_wof['available']
            bad_services = available_wof['broken']
            print("From Available Services","Services Working: ", len(good_services), "Services Not Working: ", len(bad_services))
        else:
            water = WaterMLOperations(url = url_testing)
            sites = water.GetSites()
            variables = water.GetVariables()
            print("************Passing: GETSITES***************")
            print(len(sites))

            print("************Passing: GETVARIABLES***********")
            print((variables['variables']))

            print("***********Passing: GETSITEINFO****************")
            fullSiteCodeFirstSite = sites[0]['fullSiteCode']
            siteInfo =  water.GetSiteInfo(fullSiteCodeFirstSite)
            print(len(siteInfo['siteInfo']))
            #
            # print("**********Passing: GETSITESBYBOUNDINGBOX***************")
            #
            # """
            # UNCOMMENT TO USE WITH THE epsg:3857
            # """
            # # BoundsRearranged = [-7398417.229789019,2048546.619479188,-7368453.914701229,2080306.2047316788]
            # # BoundsRearranged = [-7401666.338691997, 2060618.8113541743, -7378996.124391947, 2071003.588530944]
            # # SitesByBoundingBox = water.GetSitesByBoxObject(BoundsRearranged,'epsg:3857')
            # """
            # UNCOMMENT TO USE WITH THE epsg:4326
            # """
            # BoundsRearranged = [-66.4903,18.19699,-66.28665,18.28559]
            # SitesByBoundingBox = water.GetSitesByBoxObject(BoundsRearranged,'epsg:4326')
            # print("The number of sites in the bounding box is: ",len(SitesByBoundingBox))


            print("***********Passing: GETVALUES****************")
            if len(siteInfo['siteInfo']) > 0:

                fullVariableCodeFirstVariable = siteInfo['siteInfo'][0]['fullVariableCode']
                # methodID = siteInfo['siteInfo'][0]['methodID']
                start_date = siteInfo['siteInfo'][0]['beginDateTime'].split('T')[0]
                end_date = siteInfo['siteInfo'][0]['endDateTime'].split('T')[0]
                variableResponse = water.GetValues(fullSiteCodeFirstSite, fullVariableCodeFirstVariable, start_date, end_date)
                print("The variable and site contains values ",len(variableResponse['values']))
            else:
                print("No values for the variable and site selected")


            # return
            print("***********Passing: GETSITESBYVARIABLE****************")

            variablesTest = [variables['variables'][0]['variableCode']]
            print("Variable for testing: ", variablesTest)

            """
            USING A COOKIE CUTTER
            """
            sitesFiltered = water.GetSitesByVariable(variablesTest,sites)
            print("Sites using the GetSitesByVariable With CookieCutter", len(sitesFiltered))

            """
            WITHOUT USING A COOKIE CUTTER
            """
            sitesFiltered = water.GetSitesByVariable(variablesTest)
            print("Sites using the GetSitesByVariable No CookieCutter", len(sitesFiltered))


            if len(siteInfo['siteInfo']) > 0:
                print("**********Passing: INTERPOLATIONS***************")
                interpol_b = water.GetInterpolation(variableResponse, 'backward')
                interpol_f = water.GetInterpolation(variableResponse, 'forward')
                interpol_m = water.GetInterpolation(variableResponse, 'mean')
                print("The lenght of the interpolated values is ",len(interpol_f))
                print("The lenght of the interpolated values is",len(interpol_b))
                print("The lenght of the interpolated values is",len(interpol_m))

                print("**********Passing: GETMONTHLYAVERAGES***************")

                m_avg = water.GetMonthlyAverage(None, fullSiteCodeFirstSite, fullVariableCodeFirstVariable, start_date, end_date)
                print("Monthly Averages:",m_avg)

                print("**********Passing: GETCLUSTERSMONTHLYAVG***************")
                y_pred = water.GetClustersMonthlyAvg(sites,siteInfo['siteInfo'][0]['variableCode'])
                print("Clusters", len(y_pred))

            else:
                print("No values for the variable and site selected")


    except Exception as e:
        print(e)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("Test was sucessful")

if __name__ == "__main__":
    main()

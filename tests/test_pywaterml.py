from re import U
from tracemalloc import start
from requests import request
from pywaterml.waterML import WaterMLOperations
import pytest
# import time

# def main():
#     try:
#         for url in url_testing:
#             print("TESTING ", url)
#             single_test_quick(url[0],url[1])
#         print("Successful testing the different Endpoints")
#     except Exception as e:
#         print(e)

# def single_test_quick(url_testing,url_catalog_testing = False):
#     start_time = time.time()
#     try:
#         if url_catalog_testing:
#             print("***************WOF GetWaterOneFlowServicesInfo****************")
#             water = WaterMLOperations(url = url_testing)
#             wateroneflowservices = water.GetWaterOneFlowServicesInfo()
#             print("WaterOneFlow Services Available",wateroneflowservices)

#             print("*************WOF Available and Not available******************")
#             available_wof = water.AvailableServices()
#             # print(available_wof)
#             good_services = available_wof['available']
#             bad_services = available_wof['broken']
#             print("From Available Services","Services Working: ", len(good_services), "Services Not Working: ", len(bad_services))
#         else:
#             water = WaterMLOperations(url = url_testing)
#             sites = water.GetSites()
#             variables = water.GetVariables()
#             print("************Passing: GETSITES***************")
#             print(len(sites))

#             print("************Passing: GETVARIABLES***********")
#             print((variables['variables']))

#             print("***********Passing: GETSITEINFO****************")
#             fullSiteCodeFirstSite = sites[0]['fullSiteCode']
#             siteInfo =  water.GetSiteInfo(fullSiteCodeFirstSite)
#             print(len(siteInfo['siteInfo']))
#             #
#             # print("**********Passing: GETSITESBYBOUNDINGBOX***************")
#             #
#             # """
#             # UNCOMMENT TO USE WITH THE epsg:3857
#             # """
#             # # BoundsRearranged = [-7398417.229789019,2048546.619479188,-7368453.914701229,2080306.2047316788]
#             # # BoundsRearranged = [-7401666.338691997, 2060618.8113541743, -7378996.124391947, 2071003.588530944]
#             # # SitesByBoundingBox = water.GetSitesByBoxObject(BoundsRearranged,'epsg:3857')
#             # """
#             # UNCOMMENT TO USE WITH THE epsg:4326
#             # """
#             # BoundsRearranged = [-66.4903,18.19699,-66.28665,18.28559]
#             # SitesByBoundingBox = water.GetSitesByBoxObject(BoundsRearranged,'epsg:4326')
#             # print("The number of sites in the bounding box is: ",len(SitesByBoundingBox))


#             print("***********Passing: GETVALUES****************")
#             if len(siteInfo['siteInfo']) > 0:

#                 fullVariableCodeFirstVariable = siteInfo['siteInfo'][0]['fullVariableCode']
#                 # methodID = siteInfo['siteInfo'][0]['methodID']
#                 start_date = siteInfo['siteInfo'][0]['beginDateTime'].split('T')[0]
#                 end_date = siteInfo['siteInfo'][0]['endDateTime'].split('T')[0]
#                 variableResponse = water.GetValues(fullSiteCodeFirstSite, fullVariableCodeFirstVariable, start_date, end_date)
#                 print("The variable and site contains values ",len(variableResponse['values']))
#             else:
#                 print("No values for the variable and site selected")


#             # return
#             print("***********Passing: GETSITESBYVARIABLE****************")

#             variablesTest = [variables['variables'][0]['variableCode']]
#             print("Variable for testing: ", variablesTest)

#             """
#             USING A COOKIE CUTTER
#             """
#             sitesFiltered = water.GetSitesByVariable(variablesTest,sites)
#             print("Sites using the GetSitesByVariable With CookieCutter", len(sitesFiltered))

#             """
#             WITHOUT USING A COOKIE CUTTER
#             """
#             sitesFiltered = water.GetSitesByVariable(variablesTest)
#             print("Sites using the GetSitesByVariable No CookieCutter", len(sitesFiltered))


#             if len(siteInfo['siteInfo']) > 0:
#                 print("**********Passing: INTERPOLATIONS***************")
#                 interpol_b = water.GetInterpolation(variableResponse, 'backward')
#                 interpol_f = water.GetInterpolation(variableResponse, 'forward')
#                 interpol_m = water.GetInterpolation(variableResponse, 'mean')
#                 print("The lenght of the interpolated values is ",len(interpol_f))
#                 print("The lenght of the interpolated values is",len(interpol_b))
#                 print("The lenght of the interpolated values is",len(interpol_m))

#                 print("**********Passing: GETMONTHLYAVERAGES***************")

#                 m_avg = water.GetMonthlyAverage(None, fullSiteCodeFirstSite, fullVariableCodeFirstVariable, start_date, end_date)
#                 print("Monthly Averages:",m_avg)

#                 print("**********Passing: GETCLUSTERSMONTHLYAVG***************")
#                 y_pred = water.GetClustersMonthlyAvg(sites,siteInfo['siteInfo'][0]['variableCode'])
#                 print("Clusters", len(y_pred))

#             else:
#                 print("No values for the variable and site selected")


#     except Exception as e:
#         print(e)
#     print("--- %s seconds ---" % (time.time() - start_time))
#     print("Test was sucessful")


# url_testing_service = [
#     "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL",
#     #"http://hydroportal.cuahsi.org/CALVIN_HHS/cuahsi_1_1.asmx?WSDL",
#     #"http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-arctic/cuahsi_1_1.asmx?WSDL",
#     #"http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-plata/cuahsi_1_1.asmx?WSDL",
#     "http://gs-service-production.geodab.eu/gs-service/services/essi/view/gs-view-and(whos-country,gs-view-country(RUS))/cuahsi_1_1.asmx?WSDL"
# ]
# params_services = [
#     {
#        'url': "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL",
#        'variables':[0,1],
#        'sites':[0,1],
#    },
#    {
#        'url': "http://gs-service-production.geodab.eu/gs-service/services/essi/view/gs-view-and(whos-country,gs-view-country(RUS))/cuahsi_1_1.asmx?WSDL",
#        'variables':[0,1],
#        'sites':[0,1],
#    }

# ]

# @pytest.fixture    
# def siteInfo(sites,scope="class"):
#     fullSiteCodeFirstSite = sites[0]['fullSiteCode']
#     siteInfo =  water.GetSiteInfo(fullSiteCodeFirstSite)
#     return siteInfo

# @pytest.fixture(params=[0,1])    
# def siteInfo(request,sites,scope="class"):
#     fullSiteCodeFirstSite = sites[request.params]['fullSiteCode']
#     siteInfo =  water.GetSiteInfo(fullSiteCodeFirstSite)
#     return siteInfo




url_dummy = 'http://hydroportal.cuahsi.org/CALVIN_HHS/cuahsi_1_1.asmx?WSDL'


params_catalog =[
    "http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-country/hiscentral.asmx/GetWaterOneFlowServiceInfo",
    "http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-transboundary/hiscentral.asmx/GetWaterOneFlowServiceInfo"
]

params_services = [
    "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL",
    "http://gs-service-production.geodab.eu/gs-service/services/essi/view/gs-view-and(whos-country,gs-view-country(RUS))/cuahsi_1_1.asmx?WSDL"
]



@pytest.fixture(params=params_catalog)
def water_catalog(request,scope="class"):
    water = WaterMLOperations(url = request.params)
    return water

@pytest.fixture(params=params_services)
def water(request,scope="class"):
    water = WaterMLOperations(url = request.params)
    return water

@pytest.fixture    
def sites(water,scope="class"):
    sites = water.GetSites()
    return sites

@pytest.fixture(params=[0,1])    
def fullSiteCode(request,sites,scope="class"):
    return sites[request.params]['fullSiteCode']

@pytest.fixture(params=[0,1])    
def variableCodeMetaData(request,siteInfo,scope="class"):
    code = siteInfo['siteInfo'][request.params]['fullVariableCode']
    start_date = siteInfo['siteInfo'][request.params]['beginDateTime'].split('T')[0]
    end_date = siteInfo['siteInfo'][request.params]['endDateTime'].split('T')[0]
    return [code,start_date, end_date] 

@pytest.fixture    
def siteInfo(water,fullSiteCode,scope="class"):
    siteInfo =  water.GetSiteInfo(fullSiteCode)
    return siteInfo



class TestWaterMLCatalogs:
    @pytest.mark.parametrize("catalog_url",params_catalog)
    def TestAddService(self,catalog_url):
        water_catalog = WaterMLOperations()
        assert water_catalog.AddService(url = catalog_url) == True, f'{catalog_url} service added successfully'
    
    @pytest.mark.parametrize("catalog_url",params_catalog)
    def TestChangeService(self,catalog_url):
        water_catalog = WaterMLOperations(url=url_dummy)
        assert water_catalog.ChangeService(url=catalog_url) == True, f'{catalog_url} service changed successfully'
    
    def TestAvailableServices(self,water_catalog):
        services = water_catalog.AvailableServices()
        assert 'available' in services, f'Available {len(services["available"])} Sevices and Broken {len(services["broken"])} Services'
    
    def TestGetWaterOneFlowServicesInfo(self,water_catalog):
        services = water_catalog.GetWaterOneFlowServicesInfo()
        assert len(services) > 0, f'Retrieved {len(services)} Services'


class TestWaterMLViewsCommonFunctions:
 
    def TestGetSites(self,sites):
        assert sites, f'Retrieved {len(sites)} Sites'

    def TestGetVariables(water):
        variables = water.GetVariables()
        assert len(variables['variables']) > 0, f'Retrieved {len(variables["variables"])} variables'
        
    def TestGetSiteInfo(sites):
        fullSiteCodeFirstSite = sites[0]['fullSiteCode']
        siteInfo =  water.GetSiteInfo(fullSiteCodeFirstSite)
        assert len(siteInfo['siteInfo']) > 0, f'Retrieved {len(siteInfo["siteInfo"])} variables'
    
    def TestGetSiteInfo(siteInfo):
        assert len(siteInfo['siteInfo']) > 0, f'Retrieved {len(siteInfo["siteInfo"])} variables'
        
    def TestGetValues(water,fullSiteCode,variableCodeMetaData):
        fullVariableCodeFirstVariable = variableCodeMetaData[0]
        start_date = variableCodeMetaData[1]
        end_date = variableCodeMetaData[2]
        variableResponse = water.GetValues(fullSiteCode, fullVariableCodeFirstVariable, start_date, end_date)
        assert 'values' in variableResponse, f'Retrieved {len(variableResponse["values"])} data points'



class TestWaterMLViewsExtraFunctions:

    def TestGetSitesBoundingBox(self):
        return
    def TestGetSitesByVariables(self):
        pass
    def TestGetInterpolation(self):
        pass
    def TestGetClusters(self):
        pass
    def TestGetMonthlyAverages(self):
        pass

from pywaterml.waterML import WaterMLOperations
import time
url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
water = WaterMLOperations(url = url_testing)



url_testing = [
    ["http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-country/hiscentral.asmx/GetWaterOneFlowServiceInfo",True],
    ["http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-transboundary/hiscentral.asmx/GetWaterOneFlowServiceInfo",True],
    ["http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL", False],
    # ["http://hydroportal.cuahsi.org/CALVIN_HHS/cuahsi_1_1.asmx?WSDL", False],
    # ["http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-arctic/cuahsi_1_1.asmx?WSDL", False],
    # ["http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-plata/cuahsi_1_1.asmx?WSDL", False],
    ["http://gs-service-production.geodab.eu/gs-service/services/essi/view/gs-view-and(whos-country,gs-view-country(RUS))/cuahsi_1_1.asmx?WSDL", False]

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


# def main():
#     print("** Starting test using the http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL endpoint **")
#     start_time = time.time()
#
#     try:
#         print("************TESTING THE GETVARIABLES() FUNCTION***************")
#         sites = water.GetSites()
#         print("SUCCESS, number of sites imported ",len(sites))
#     except:
#         print("GetSites() function is not passing the test.")
#     try:
#         print("************TESTING THE GETVARIABLES() FUNCTION ***********")
#         variables = water.GetVariables()
#         print("SUCCESS, GetVariables() function is working, the number of variables", len(variables) )
#     except:
#         print("GetVariables() function is not passing the test.")
#     try:
#         print("***********TESTING GETSITEINFO() FUNCTION****************")
#         site_full_code = "Para_La_Naturaleza:Rio_Toro_Negro"
#         siteInfo =  water.GetSiteInfo(site_full_code)
#         print("SUCESS, GetSiteInfo funtion is working")
#     except:
#         print("GetSiteInfo() function is not passing the test.")
#     try:
#         print("***********TESTING GETVALUES() FUNCTION****************")
#         network = sites[0]['network']
#         firstVariableCode = siteInfo[0]['code']
#         variable_full_code = network + ":" + firstVariableCode
#         methodID = siteInfo[0]['methodID']
#         start_date = siteInfo[0]['timeInterval']['beginDateTime'].split('T')[0]
#         end_date = siteInfo[0]['timeInterval']['endDateTime'].split('T')[0]
#         variableResponse = water.GetValues(site_full_code, variable_full_code, methodID, start_date, end_date)
#         print("SUCESS, GetValues() is passing the test with ", len(variableResponse), "values")
#     except:
#         print("GetValues() function is not passing the test.")
#     try:
#         print("***********TESTING GETINTERPOLATION() FUNCTION****************")
#         interpol_b = water.GetInterpolation(variableResponse['values'], 'backward')
#         interpol_f = water.GetInterpolation(variableResponse['values'], 'forward')
#         interpol_m = water.GetInterpolation(variableResponse['values'], 'mean')
#         print("SUCCESS GetInterpolation function for mean interpolation is working ",len(interpol_f), "forward interpolated values")
#         print("SUCCESS GetInterpolation function for mean interpolation is working ",len(interpol_b), "backward interpolated values")
#         print("SUCCESS GetInterpolation function for mean interpolation is working ",len(interpol_m), "mean interpolated values")
#     except:
#         print("GetInterpolation() function is not passing the test.")
#
#     try:
#         print("***********TESTING GETMONTHLYAVERAGE() FUNCTION****************")
#         m_avg = water.GetMonthlyAverage(None, site_full_code, variable_full_code, methodID, start_date, end_date)
#         print("SUCCESS GetMonthlyAverage() function working ",len(m_avg), " monthly averages values")
#     except:
#         print("GetMonthlyAverage() function is not passing the test")
#
#     try:
#         print("***********TESTING GETCLUSTERMONTHLYAVG() FUNCTION****************")
#         y_pred = water.GetClustersMonthlyAvg(sites,siteInfo[0]['name'])
#         print("SUCCESS GetClustersMonthlyAvg() function is not working ")
#     except:
#         print("GetClustersMonthlyAvg() function is not passing the test.")
#
#     try:
#         print("***********TESTING GETSITESBYBOXOBJECT() FUNCTION****************")
#         """
#         UNCOMMENT TO USE WITH THE epsg:3857
#         """
#         # BoundsRearranged = [-7398417.229789019,2048546.619479188,-7368453.914701229,2080306.2047316788]
#         # BoundsRearranged = [-7401666.338691997, 2060618.8113541743, -7378996.124391947, 2071003.588530944]
#         # SitesByBoundingBox = water.GetSitesByBoxObject(BoundsRearranged,'epsg:3857')
#         """
#         UNCOMMENT TO USE WITH THE epsg:4326
#         """
#         BoundsRearranged = [-66.4903,18.19699,-66.28665,18.28559]
#         SitesByBoundingBox = water.GetSitesByBoxObject(BoundsRearranged,'epsg:4326')
#
#         print("SUCCESS GetSitesByBoxObject() function is working ",len(SitesByBoundingBox)," sites imported" )
#     except:
#         print("GetSitesByBoxObject() function is not working ")
#     try:
#         print("***********TESTING GETSITESBYVARIABLE() FUNCTION WITH A COOKIECUTTER WITHOUT COOKIECUTTER****************")
#         variablesTest = [variables[0]]
#         """
#         USING A COOKIE CUTTER
#         """
#         sitesFiltered = water.GetSitesByVariable(variablesTest,sites)
#         print("SUCCESS GetSitesByVariable() is working",len(sitesFiltered), "sites imported using cookiecutter")
#     except:
#         print("GetSitesByVariable() function is not working with cookiecutter")
#     try:
#         print("***********TESTING GETSITESBYVARIABLE() FUNCTION WITHOUT A COOKIECUTTER WITHOUT COOKIECUTTER****************")
#         """
#         WITHOUT USING A COOKIE CUTTER
#         """
#         sitesFiltered = water.GetSitesByVariable(variablesTest)
#         print("SUCCESS GetSitesByVariable() is working",len(sitesFiltered), "sites imported without using cookiecutter")
#     except:
#         print("GetSitesByVariable() function is not working withou cookiecutter")
#
#     print("--- %s seconds ---" % (time.time() - start_time))
#     print("Test was sucessful")
#
#     print("SECOND TEST RUNNING WITH NEW ENDPOINT")
#     start_time = time.time()
#     print("** Starting test using the http://hydroportal.cuahsi.org/CALVIN_HHS/cuahsi_1_1.asmx?WSDL endpoint **")
#     water.ChangeEndpoint("http://hydroportal.cuahsi.org/CALVIN_HHS/cuahsi_1_1.asmx?WSDL")
#     try:
#         print("************TESTING THE GETVARIABLES() FUNCTION***************")
#         sites = water.GetSites()
#         print("SUCCESS, number of sites imported ",len(sites))
#     except:
#         print("GetSites() function is not passing the test.")
#
#     try:
#         print("************TESTING THE GETVARIABLES() FUNCTION ***********")
#         variables = water.GetVariables()
#         print("SUCCESS, GetVariables() function is working, the number of variables", len(variables) )
#     except:
#         print("GetVariables() function is not passing the test.")
#
#     try:
#         print("***********TESTING GETSITEINFO() FUNCTION****************")
#         site_full_code = "Para_La_Naturaleza:Rio_Toro_Negro"
#         siteInfo =  water.GetSiteInfo(site_full_code)
#         print("SUCESS, GetSiteInfo funtion is working")
#     except:
#         print("GetSiteInfo() function is not passing the test.")
#
#     try:
#         print("***********TESTING GETVALUES() FUNCTION****************")
#         network = sites[0]['network']
#         firstVariableCode = siteInfo[0]['code']
#         variable_full_code = network + ":" + firstVariableCode
#         methodID = siteInfo[0]['methodID']
#         start_date = siteInfo[0]['timeInterval']['beginDateTime'].split('T')[0]
#         end_date = siteInfo[0]['timeInterval']['endDateTime'].split('T')[0]
#         variableResponse = water.GetValues(site_full_code, variable_full_code, methodID, start_date, end_date)
#         print("SUCESS, GetValues() is passing the test with ", len(variableResponse), "values")
#     except:
#         print("GetValues() function is not passing the test")
#     try:
#         print("***********TESTING GETINTERPOLATION() FUNCTION****************")
#         interpol_b = water.GetInterpolation(variableResponse['values'], 'backward')
#         interpol_f = water.GetInterpolation(variableResponse['values'], 'forward')
#         interpol_m = water.GetInterpolation(variableResponse['values'], 'mean')
#         print("SUCCESS GetInterpolation function for mean interpolation is working ",len(interpol_f), "forward interpolated values")
#         print("SUCCESS GetInterpolation function for mean interpolation is working ",len(interpol_b), "backward interpolated values")
#         print("SUCCESS GetInterpolation function for mean interpolation is working ",len(interpol_m), "mean interpolated values")
#     except:
#         print("GetInterpolation() function is not passing the test.")
#
#     try:
#         print("***********TESTING GETMONTHLYAVERAGE() FUNCTION****************")
#         m_avg = water.GetMonthlyAverage(None, site_full_code, variable_full_code, methodID, start_date, end_date)
#         print("SUCCESS GetMonthlyAverage() function working ",len(m_avg), " monthly averages values")
#     except:
#         print("GetMonthlyAverage() function is not passing the test")
#
#     try:
#         print("***********TESTING GETCLUSTERMONTHLYAVG() FUNCTION****************")
#         y_pred = water.GetClustersMonthlyAvg(sites,siteInfo[0]['name'])
#         print("SUCCESS GetClustersMonthlyAvg() function is not working ")
#     except:
#         print("GetClustersMonthlyAvg() function is not passing the test.")
#
#     try:
#         print("***********TESTING GETSITESBYBOXOBJECT() FUNCTION****************")
#         """
#         UNCOMMENT TO USE WITH THE epsg:3857
#         """
#         # BoundsRearranged = [-7398417.229789019,2048546.619479188,-7368453.914701229,2080306.2047316788]
#         # BoundsRearranged = [-7401666.338691997, 2060618.8113541743, -7378996.124391947, 2071003.588530944]
#         # SitesByBoundingBox = water.GetSitesByBoxObject(BoundsRearranged,'epsg:3857')
#         """
#         UNCOMMENT TO USE WITH THE epsg:4326
#         """
#         BoundsRearranged = [-66.4903,18.19699,-66.28665,18.28559]
#         SitesByBoundingBox = water.GetSitesByBoxObject(BoundsRearranged,'epsg:4326')
#
#         print("SUCCESS GetSitesByBoxObject() function is working ",len(SitesByBoundingBox)," sites imported" )
#     except:
#         print("GetSitesByBoxObject() function is not working ")
#
#     try:
#         print("***********TESTING GETSITESBYVARIABLE() FUNCTION WITH A COOKIECUTTER WITHOUT COOKIECUTTER****************")
#         variablesTest = [variables[0]]
#         """
#         USING A COOKIE CUTTER
#         """
#         sitesFiltered = water.GetSitesByVariable(variablesTest,sites)
#         print("SUCCESS GetSitesByVariable() is working",len(sitesFiltered), "sites imported using cookiecutter")
#     except:
#         print("GetSitesByVariable() function is not working with cookiecutter")
#
#     try:
#         print("***********TESTING GETSITESBYVARIABLE() FUNCTION WITHOUT A COOKIECUTTER WITHOUT COOKIECUTTER****************")
#         """
#         WITHOUT USING A COOKIE CUTTER
#         """
#         sitesFiltered = water.GetSitesByVariable(variablesTest)
#         print("SUCCESS GetSitesByVariable() is working",len(sitesFiltered), "sites imported without using cookiecutter")
#     except:
#         print("GetSitesByVariable() function is not working withou cookiecutter")
#
#     print("--- %s seconds ---" % (time.time() - start_time))
#     print("Test was sucessful")

if __name__ == "__main__":
    main()

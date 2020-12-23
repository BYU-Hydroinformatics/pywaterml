from pywaterml.waterML import WaterMLOperations
import time
url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
water = WaterMLOperations(url = url_testing)

def main():
    print("** Starting test using the http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL endpoint **")
    start_time = time.time()

    try:
        print("************TESTING THE GETVARIABLES() FUNCTION***************")
        sites = water.GetSites()
        print("SUCCESS, number of sites imported ",len(sites))
    except:
        print("GetSites() function is not passing the test.")
    try:
        print("************TESTING THE GETVARIABLES() FUNCTION ***********")
        variables = water.GetVariables()
        print("SUCCESS, GetVariables() function is working, the number of variables", len(variables) )
    except:
        print("GetVariables() function is not passing the test.")
    try:
        print("***********TESTING GETSITEINFO() FUNCTION****************")
        site_full_code = "Para_La_Naturaleza:Rio_Toro_Negro"
        siteInfo =  water.GetSiteInfo(site_full_code)
        print("SUCESS, GetSiteInfo funtion is working")
    except:
        print("GetSiteInfo() function is not passing the test.")
    try:
        print("***********TESTING GETVALUES() FUNCTION****************")
        network = sites[0]['network']
        firstVariableCode = siteInfo[0]['code']
        variable_full_code = network + ":" + firstVariableCode
        methodID = siteInfo[0]['methodID']
        start_date = siteInfo[0]['timeInterval']['beginDateTime'].split('T')[0]
        end_date = siteInfo[0]['timeInterval']['endDateTime'].split('T')[0]
        variableResponse = water.GetValues(site_full_code, variable_full_code, methodID, start_date, end_date)
        print("SUCESS, GetValues() is passing the test with ", len(variableResponse), "values")
    except:
        print("GetValues() function is not passing the test.")
    try:
        print("***********TESTING GETINTERPOLATION() FUNCTION****************")
        interpol_b = water.GetInterpolation(variableResponse['values'], 'backward')
        interpol_f = water.GetInterpolation(variableResponse['values'], 'forward')
        interpol_m = water.GetInterpolation(variableResponse['values'], 'mean')
        print("SUCCESS GetInterpolation function for mean interpolation is working ",len(interpol_f), "forward interpolated values")
        print("SUCCESS GetInterpolation function for mean interpolation is working ",len(interpol_b), "backward interpolated values")
        print("SUCCESS GetInterpolation function for mean interpolation is working ",len(interpol_m), "mean interpolated values")
    except:
        print("GetInterpolation() function is not passing the test.")

    try:
        print("***********TESTING GETMONTHLYAVERAGE() FUNCTION****************")
        m_avg = water.GetMonthlyAverage(None, site_full_code, variable_full_code, methodID, start_date, end_date)
        print("SUCCESS GetMonthlyAverage() function working ",len(m_avg), " monthly averages values")
    except:
        print("GetMonthlyAverage() function is not passing the test")

    try:
        print("***********TESTING GETCLUSTERMONTHLYAVG() FUNCTION****************")
        y_pred = water.GetClustersMonthlyAvg(sites,siteInfo[0]['name'])
        print("SUCCESS GetClustersMonthlyAvg() function is not working ")
    except:
        print("GetClustersMonthlyAvg() function is not passing the test.")

    try:
        print("***********TESTING GETSITESBYBOXOBJECT() FUNCTION****************")
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

        print("SUCCESS GetSitesByBoxObject() function is working ",len(SitesByBoundingBox)," sites imported" )
    except:
        print("GetSitesByBoxObject() function is not working ")
    try:
        print("***********TESTING GETSITESBYVARIABLE() FUNCTION WITH A COOKIECUTTER WITHOUT COOKIECUTTER****************")
        variablesTest = [variables[0]]
        """
        USING A COOKIE CUTTER
        """
        sitesFiltered = water.GetSitesByVariable(variablesTest,sites)
        print("SUCCESS GetSitesByVariable() is working",len(sitesFiltered), "sites imported using cookiecutter")
    except:
        print("GetSitesByVariable() function is not working with cookiecutter")
    try:
        print("***********TESTING GETSITESBYVARIABLE() FUNCTION WITHOUT A COOKIECUTTER WITHOUT COOKIECUTTER****************")
        """
        WITHOUT USING A COOKIE CUTTER
        """
        sitesFiltered = water.GetSitesByVariable(variablesTest)
        print("SUCCESS GetSitesByVariable() is working",len(sitesFiltered), "sites imported without using cookiecutter")
    except:
        print("GetSitesByVariable() function is not working withou cookiecutter")

    print("--- %s seconds ---" % (time.time() - start_time))
    print("Test was sucessful")

    print("SECOND TEST RUNNING WITH NEW ENDPOINT")
    start_time = time.time()
    print("** Starting test using the http://hydroportal.cuahsi.org/CALVIN_HHS/cuahsi_1_1.asmx?WSDL endpoint **")
    water.ChangeEndpoint("http://hydroportal.cuahsi.org/CALVIN_HHS/cuahsi_1_1.asmx?WSDL")
    try:
        print("************TESTING THE GETVARIABLES() FUNCTION***************")
        sites = water.GetSites()
        print("SUCCESS, number of sites imported ",len(sites))
    except:
        print("GetSites() function is not passing the test.")

    try:
        print("************TESTING THE GETVARIABLES() FUNCTION ***********")
        variables = water.GetVariables()
        print("SUCCESS, GetVariables() function is working, the number of variables", len(variables) )
    except:
        print("GetVariables() function is not passing the test.")

    try:
        print("***********TESTING GETSITEINFO() FUNCTION****************")
        site_full_code = "Para_La_Naturaleza:Rio_Toro_Negro"
        siteInfo =  water.GetSiteInfo(site_full_code)
        print("SUCESS, GetSiteInfo funtion is working")
    except:
        print("GetSiteInfo() function is not passing the test.")

    try:
        print("***********TESTING GETVALUES() FUNCTION****************")
        network = sites[0]['network']
        firstVariableCode = siteInfo[0]['code']
        variable_full_code = network + ":" + firstVariableCode
        methodID = siteInfo[0]['methodID']
        start_date = siteInfo[0]['timeInterval']['beginDateTime'].split('T')[0]
        end_date = siteInfo[0]['timeInterval']['endDateTime'].split('T')[0]
        variableResponse = water.GetValues(site_full_code, variable_full_code, methodID, start_date, end_date)
        print("SUCESS, GetValues() is passing the test with ", len(variableResponse), "values")
    except:
        print("GetValues() function is not passing the test")
    try:
        print("***********TESTING GETINTERPOLATION() FUNCTION****************")
        interpol_b = water.GetInterpolation(variableResponse['values'], 'backward')
        interpol_f = water.GetInterpolation(variableResponse['values'], 'forward')
        interpol_m = water.GetInterpolation(variableResponse['values'], 'mean')
        print("SUCCESS GetInterpolation function for mean interpolation is working ",len(interpol_f), "forward interpolated values")
        print("SUCCESS GetInterpolation function for mean interpolation is working ",len(interpol_b), "backward interpolated values")
        print("SUCCESS GetInterpolation function for mean interpolation is working ",len(interpol_m), "mean interpolated values")
    except:
        print("GetInterpolation() function is not passing the test.")

    try:
        print("***********TESTING GETMONTHLYAVERAGE() FUNCTION****************")
        m_avg = water.GetMonthlyAverage(None, site_full_code, variable_full_code, methodID, start_date, end_date)
        print("SUCCESS GetMonthlyAverage() function working ",len(m_avg), " monthly averages values")
    except:
        print("GetMonthlyAverage() function is not passing the test")

    try:
        print("***********TESTING GETCLUSTERMONTHLYAVG() FUNCTION****************")
        y_pred = water.GetClustersMonthlyAvg(sites,siteInfo[0]['name'])
        print("SUCCESS GetClustersMonthlyAvg() function is not working ")
    except:
        print("GetClustersMonthlyAvg() function is not passing the test.")

    try:
        print("***********TESTING GETSITESBYBOXOBJECT() FUNCTION****************")
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

        print("SUCCESS GetSitesByBoxObject() function is working ",len(SitesByBoundingBox)," sites imported" )
    except:
        print("GetSitesByBoxObject() function is not working ")

    try:
        print("***********TESTING GETSITESBYVARIABLE() FUNCTION WITH A COOKIECUTTER WITHOUT COOKIECUTTER****************")
        variablesTest = [variables[0]]
        """
        USING A COOKIE CUTTER
        """
        sitesFiltered = water.GetSitesByVariable(variablesTest,sites)
        print("SUCCESS GetSitesByVariable() is working",len(sitesFiltered), "sites imported using cookiecutter")
    except:
        print("GetSitesByVariable() function is not working with cookiecutter")

    try:
        print("***********TESTING GETSITESBYVARIABLE() FUNCTION WITHOUT A COOKIECUTTER WITHOUT COOKIECUTTER****************")
        """
        WITHOUT USING A COOKIE CUTTER
        """
        sitesFiltered = water.GetSitesByVariable(variablesTest)
        print("SUCCESS GetSitesByVariable() is working",len(sitesFiltered), "sites imported without using cookiecutter")
    except:
        print("GetSitesByVariable() function is not working withou cookiecutter")

    print("--- %s seconds ---" % (time.time() - start_time))
    print("Test was sucessful")

if __name__ == "__main__":
    main()

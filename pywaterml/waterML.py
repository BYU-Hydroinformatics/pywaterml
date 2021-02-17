from suds.client import Client
import json
import xmltodict
from bs4 import BeautifulSoup
from json import dumps, loads
from pywaterml.aux import Auxiliary
from pywaterml.analyzeData import WaterAnalityca
from pyproj import Proj, transform
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
from tslearn.metrics import dtw
from tslearn.clustering import TimeSeriesKMeans
from tslearn.utils import to_time_series, to_time_series_dataset

class WaterMLOperations():
    """
    This class represents the WaterML object that will be able to fetch and analyze Data from 'WaterML' and 'WaterOneFlow' Web Services

    Args:
        url: Endpoint that complies to the SOAP protocol
    """
    def __init__(self,url = None):
        self.url = url
        self.client = Client(url, timeout= 500)
        self.aux = Auxiliary()

    def AddEndpoint(self,url):
        """
        Add a endpoint to the WaterMLOperations class. It can have any endpoint that uses the SOAP protocol.

        Args:
            url: endpoint that complies to the SOAP protocol
        Returns:
            None
        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations()
            data = water.AddEndpoint(url_testing)
        """
        if self.url is None:
            self.url = url
            self.client = Client(url, timeout= 500)
        else:
            print("There is already an enpoint, if you want to change the endpoint try ChangeEndpoint() function")
        pass

    def ChangeEndpoint(self,url):
        """
        Change the endpoint of a WaterMLOperations class. The current endpoint can be changed by any endpoint that uses the SOAP protocol.

        Args:
            url: endpoint that complies to the SOAP protocol

        Returns:
            None

        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            data = water.ChangeEndpoint("http://128.187.106.131/app/index.php/dr/services/cuahsi_1_1.asmx?WSDL")
        """
        if self.url is not None:
            self.url = url
            self.client = Client(url, timeout= 500)
        else:
            print("There is no endpoint, please before changing an endpoint add one with AddEndpoint() function")
        pass

    def GetSites(self, format="json"):
        """
        Get all the sites from a endpoint that complies to the SOAP protocol. The GetSites() function is similar to the GetSites() WaterML function.

        Args:
            format: format of the response (json or waterML)

        Returns:
            An array of objects that represent each site. The structure of the response is the following

        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            sites = water.GetSites()
        """
        try:
            sites = self.client.service.GetSites('[:]')
        except Exception as error:
            print(error)
        if format is "waterml":
            return sites
        sites_json={}
        if isinstance(sites, str):
            sites_dict = xmltodict.parse(sites)
            sites_json_object = json.dumps(sites_dict)
            sites_json = json.loads(sites_json_object)
        else:
            sites_json_object = suds_to_json(sites)
            sites_json = json.loads(sites_json_object)

        sites_object = Auxiliary._parseJSON(sites_json)

        if format is "json":
            return sites_object
        elif format is "csv":
            df = pd.DataFrame.from_dict(sites_object)
            csv_sites = df.to_csv(index=False)
            # csv_sites.to_csv("/home/elkin/Projects/condaPackages/pywaterml/tests")
            return csv_sites
        else:
            return print("the only supported formats are json, csv, and waterml")

    def GetSitesByBoxObject(self,ext_list, inProjection, format="json"):
        """
        Get all the sites from a bounding box from a endpoint that complies to the SOAP protocol. The GetSitesByBoxObject() function is similar to the GetSitesByBoxObject() WaterML function.

        Args:
            ext_list: Array of bounding box coordinates in a given projection.
            inProjection: Projection from the array of coordinates of the given bounding box.
            format: format of the response (json or waterML)

        Returns:
            An array of objects that represent each site. The structure of the response is the following

        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            ## use with epsg:4326 ##
            BoundsRearranged = [-66.4903,18.19699,-66.28665,18.28559]
            sites = water.GetSitesByBoxObject(BoundsRearranged,'epsg:4326')
        """

        inProj = Proj(init=inProjection)
        outProj = Proj(init='epsg:4326')

        minx, miny = ext_list[0], ext_list[1]
        maxx, maxy = ext_list[2], ext_list[3]
        x1, y1 = transform(inProj, outProj, minx, miny)
        x2, y2 = transform(inProj, outProj, maxx, maxy)
        try:
            bbox = self.client.service.GetSitesByBoxObject(
                x1, y1, x2, y2, '1', '')
        except Exception as error:
            print(error)
            return([])
        if format is "waterml":
            return bbox

        wml_sites = self.aux._parseWML(bbox)
        if format is "json":
        # sites_parsed_json = json.dumps(wml_sites)
        # return sites_parsed_json
            return wml_sites
        elif format is "csv":
            df = pd.DataFrame.from_dict(wml_sites)
            csv_sites = df.to_csv(index=False)
            return csv_sites
        else:
            return print("the only supported formats are json, csv, and waterml")

    def GetVariables(self, format="json"):
        """
        Get all the variables from a endpoint that complies to the SOAP protocol. GetVariables() function is similar to the GetVariables() WaterML function

        Args:
            format: format of the response (json or waterML)

        Returns:
            An array of strings representing the variables from the enpoint. The structure of the response is the following

            ['Water depth, averaged', 'Discharge', 'Velocity']

        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            variables = water.GetVariables()

        """
        return_array = []
        try:
            variables = self.client.service.GetVariables('[:]')
            if format is 'waterml':
                return variables
            variables_dict = xmltodict.parse(variables)
            variables_dict_object = json.dumps(variables_dict)

            variables_json = json.loads(variables_dict_object)
            array_variables = variables_json['variablesResponse']['variables']['variable']

            if isinstance(array_variables,type([])):
                return_object = {}
                for one_variable in array_variables:
                    return_object = self.aux._getVariablesHelper(one_variable, return_obj)
                    # return_object['variableName'] = one_variable['variableName']
                    # return_object['variableCode'] = one_variable['variableCode']['#text']
                    # return_object['valueType']= one_variable['valueType']
                    # return_object['dataType']= one_variable['dataType']
                    # return_object['generalCategory'] = one_variable['generalCategory']
                    # return_object['sampleMedium'] = one_variable['sampleMedium']
                    # return_object['unitName'] = one_variable['unit']['unitName']
                    # return_object['unitType'] = one_variable['unit']['unitType']
                    # return_object['unitAbbreviation'] = one_variable['unit']['unitAbbreviation']
                    # return_object['noDataValue'] = one_variable['noDataValue']
                    # return_object['isRegular'] = one_variable['variableCode']['@default']
                    # return_object['timeUnitName'] = one_variable['timeScale']['unit']['unitName']
                    # return_object['timeUnitAbbreviation'] = one_variable['timeScale']['unit']['unitAbbreviation']
                    # return_object['timeSupport'] = one_variable['timeScale']['timeSupport']
                    # return_object['speciation'] = one_variable['speciation']
                    return_array.append(return_object)

            if isinstance(array_variables,dict):
                return_object = {}
                return_object = self.aux._getVariablesHelper(array_variables, return_obj)

                # return_object['variableName'] = array_variables['variableName']
                # return_object['variableCode'] = array_variables['variableCode']['#text']
                # return_object['valueType']= array_variables['valueType']
                # return_object['dataType']= array_variables['dataType']
                # return_object['generalCategory'] = array_variables['generalCategory']
                # return_object['sampleMedium'] = array_variables['sampleMedium']
                # return_object['unitName'] = array_variables['unit']['unitName']
                # return_object['unitType'] = array_variables['unit']['unitType']
                # return_object['unitAbbreviation'] = array_variables['unit']['unitAbbreviation']
                # return_object['noDataValue'] = array_variables['noDataValue']
                # return_object['isRegular'] = array_variables['variableCode']['@default']
                # return_object['timeUnitName'] = array_variables['timeScale']['unit']['unitName']
                # return_object['timeUnitAbbreviation'] = array_variables['timeScale']['unit']['unitAbbreviation']
                # return_object['timeSupport'] = array_variables['timeScale']['timeSupport']
                # return_object['speciation'] = array_variables['speciation']
                return_array.append(return_object)

            if format is "json":
                json_response = {
                    'variables':return_array
                }
                return(json_response)
            elif format is "csv":
                df = pd.DataFrame.from_dict(return_array)
                # print(df)
                csv_siteInfo = df.to_csv(index=False)
                return csv_siteInfo
            else:
                return print("the only supported formats are json, csv, and waterml")
        except Exception as error:
            print(error)
            return_array = []
            return return_array


        # return array_final_variables

    def GetSiteInfo(self,site_full_code, format ="json"):
        """
        Get the information of a given site. GetSiteInfo() function is similar to the GetSiteInfo() WaterML function.

        Args:
            site_full_code: A string representing the full code of the given site following the structure
                - site_full_code = site network + ":" + site code
        Returns:
            An array of objects that represent information for each site variable. Each object has the following properties

            - name: variable name
            - code: varibale code
            - count: time series data points for the given variable
            - methodID: method for data extraction for the given variable
            - description: object containing different properties for the description of the given variable in each site.
                - organization: organization responsible for the data extraction of the site.
                - sourceDescription: description of the source from the data extraction of the site
                - citation: site citation for all the sites
            - timeInterval
                - beginDateTime: beginning date time for the time series of the variable
                - endDateTime: end date time for the time series of the variable
                - beginDateTimeUTC: beginning date time for the time series of the variable in UTC format
                - endDateTimeUTC: end date time for the time series of the variable in UTC format

            The structure of the response is the following
                - name
                - code
                - count
                - description
                - organization
                - sourceDescription
                - citation
                - timeInterval


        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            sites = water.GetSites()
            firstSiteCode = sites[0]['sitecode']
            network = sites[0]['network']
            site_full_code = network +":"+firstSiteCode
            siteInfo = water.GetSiteInfo(site_full_code)
        """
        site_info_Mc = self.client.service.GetSiteInfo(site_full_code)
        if format is 'waterml':
            return site_info_Mc
        site_info_Mc_dict = xmltodict.parse(site_info_Mc)
        site_info_Mc_json_object = json.dumps(site_info_Mc_dict)
        site_info_Mc_json = json.loads(site_info_Mc_json_object)


        try:
            object_methods = site_info_Mc_json['sitesResponse']['site']['seriesCatalog']['series']
            object_siteInfo = site_info_Mc_json['sitesResponse']['site']['siteInfo']
            return_array = []
            if(isinstance(object_methods,(dict))):
                return_obj = self.aux._getSiteInfoHelper(object_siteInfo,object_methods)
                return_array.append(return_obj)

            else:
                for object_method in object_methods:
                    return_obj = self.aux._getSiteInfoHelper(object_siteInfo,object_method)
                    return_array.append(return_obj)
            if format is "json":
                json_response = {
                    'siteInfo':return_array
                }
                return json_response
            elif format is "csv":
                df = pd.DataFrame.from_dict(return_array)
                csv_siteInfo = df.to_csv(index=False)
                return csv_siteInfo
            else:
                return print("the only supported formats are json, csv, and waterml")
        except KeyError as ke:
            print(ke)
            print("No series for the site")
            return_array = []
            return return_array
        return return_array

    def GetValues(self,site_full_code, variable_full_code, start_date, end_date, methodCode = None, qualityControlLevelCode = None, format = 'json'):
        """
        Get the specific values for an specific variable in a site. GetValues() function is similar to the GetValues() WaterML function.

        Args:
            site_full_code: A string representing the full code of the given site following the structure
                - site_full_code = site network + ":" + site code

            variable_full_code: A string representing the full code of the given variable following the structure
                - variable_full_code = site network + ":" + variable code

            methodID: method for data extraction for the given variable
            start_date: beginning date time for the time series of the variable
            end_date: end date time for the time series of the variable

        Returns:
            An object containing properties for the time series values for the given variable in the given site. The structure of the response is the following

                - variable: variable name
                - unit: units of the values
                - title: title of the time series values
                - values: an array of arrays containing [date, value]

            An example of the response is:
            {'variable': 'Water depth, averaged', 'unit': 'm', 'title': 'Water depth, averaged (m) vs Time', 'values': [['2013-08-03 05:00:00', 0.1815], ['2013-09-07 05:00:00', 0.187], ['2013-10-05 05:00:00', 0.226], ['2013-11-02 05:00:00', 0.1535], ['2013-12-07 05:00:00', 0.231], ['2014-01-11 05:00:00', 0.15525], ['2014-02-01 05:00:00', 0.124875], ['2014-03-01 05:00:00', 0.0], ['2014-04-05 05:00:00', 0.1145], ['2014-05-03 05:00:00', 0.0877], ['2014-06-07 05:00:00', 0.0], ['2014-07-05 05:00:00', 0.09375], ['2014-09-06 05:00:00', 0.12175], ['2014-10-04 05:00:00', 0.10325], ['2014-11-01 05:00:00', 0.1693], ['2014-12-06 05:00:00', 0.187], ['2015-01-03 05:00:00', 0.1285], ['2015-02-07 05:00:00', 0.125], ['2015-03-07 05:00:00', 0.159], ['2015-04-04 05:00:00', 0.14]]}
        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            sites = water.GetSites()
            firstSiteCode = sites[0]['sitecode']
            network = sites[0]['network']
            site_full_code = network +":"+firstSiteCode
            siteInfo = water.GetSiteInfo(site_full_code)
            firstVariableCode = siteInfo[0]['code']
            variable_full_code = network + ":" + firstVariableCode
            methodID = siteInfo[0]['methodID']
            start_date = siteInfo[0]['timeInterval']['beginDateTime'].split('T')[0]
            end_date = siteInfo[0]['timeInterval']['endDateTime'].split('T')[0]
            variableResponse= water.GetValues(site_full_code, variable_full_code, methodID, start_date, end_date)
        """
        values = self.client.service.GetValues(
            site_full_code, variable_full_code, start_date, end_date, "")

        if format is "waterml":
            return values
        values_dict = xmltodict.parse(values)
        values_json_object = json.dumps(values_dict)

        values_json = json.loads(values_json_object)
        times_series = {}
        return_array = []
        try:
            if 'timeSeriesResponse' in values_json:
                times_series = values_json['timeSeriesResponse']['timeSeries']
                if times_series['values'] is not None:

                    for j in times_series['values']:

                        if j == "value":
                            if type(times_series['values']['value']) is list:
                                json_response = {}
                                for k in times_series['values']['value']:
                                    try:
                                        if k['@methodCode'] == methodCode and methodCode is not None:
                                            json_response = self.aux._getValuesHelper2(times_series,json_response)
                                            json_response = self.aux._getValuesHelper(k,json_response)
                                            return_array.append(json_response)
                                            json_response = {}

                                        if k['@qualityControlLevelCode'] == qualityControlLevelCode and qualityControlLevelCode is not None:
                                            json_response = self.aux._getValuesHelper2(times_series,json_response)
                                            json_response = self.aux._getValuesHelper(k,json_response)
                                            return_array.append(json_response)
                                            json_response = {}

                                        else:
                                            json_response = self.aux._getValuesHelper2(times_series,json_response)
                                            json_response = self.aux._getValuesHelper(k,json_response)
                                            return_array.append(json_response)
                                            json_response = {}

                                    except KeyError as ke:  # The Key Error kicks in when there is only one timeseries
                                        print(ke)
                                        json_response = self.aux._getValuesHelper2(times_series,json_response)
                                        json_response = self.aux._getValuesHelper(k,json_response)
                                        json_response = {}
                                        return_array.append(json_response)


                            else:  # The else statement is executed is there is only one value in the timeseries
                                k = times_series['values']['value']
                                try:
                                    if k['@methodCode'] == methodCode and methodCode is not None:
                                        json_response = {}
                                        json_response = self.aux._getValuesHelper2(times_series,json_response)
                                        json_response = self.aux._getValuesHelper(k,json_response)
                                        return_array.append(json_response)

                                    if k['@qualityControlLevelCode'] == qualityControlLevelCode and qualityControlLevelCode is not None:
                                        json_response = {}
                                        json_response = self.aux._getValuesHelper2(times_series,json_response)
                                        json_response = self.aux._getValuesHelper(k,json_response)
                                        return_array.append(json_response)

                                    else:
                                        json_response = self.aux._getValuesHelper2(times_series,json_response)
                                        json_response = self.aux._getValuesHelper(k,json_response)
                                        return_array.append(json_response)

                                except KeyError as ke:
                                    json_response = {}
                                    json_response = self.aux._getValuesHelper2(times_series,json_response)
                                    json_response = self.aux._getValuesHelper(k,json_response)
                                    return_array.append(json_response)

        except KeyError as error:
            print(error)

        if format is "json":
            json_response = {
                'values': return_array
            }
            return(json_response)
        elif format is "csv":
            df = pd.DataFrame.from_dict(return_array)
            # print(df)
            csv_values = df.to_csv(index=False)
            return csv_values
        else:
            return print("the only supported formats are json, csv, and waterml")

        return graph_json

    def GetSitesByVariable(self,specific_variables_codes,cookiCutter = None, format='json'):
        """
        Get the specific sites according to a variable search array from a endpoint that complies to the SOAP protocol. The GetSitesByVariable() is an addition to the WaterML functions
        because it allows the user to retrieve sites that contains the epecific site/s.

        Args

            specific_variables: An array of strings representing a list of variables that will serve as a filter when retrieving sites.
            cookiCutter: A list containing the different information from each site. It can be the response of the GetSites() or GetSitesByBoxObject() functions.
            if the cookiCutter is not specified, the function will filter all the functions calling GetSites() internally.

        Returns:

            An array of objects that represent each site. The structure of the response is the following

            [{'sitename': 'Río Toro Negro', 'latitude': '18.28559', 'longitude': '-66.4903', 'sitecode': 'Rio_Toro_Negro', 'network': 'Para_La_Naturaleza', 'service': 'SOAP'}, {'sitename': 'Quebrada Batista', 'latitude': '18.19699', 'longitude': '-66.32992', 'sitecode': 'Quebrada_Batista', 'network': 'Para_La_Naturaleza', 'service': 'SOAP'}, {'sitename': 'Río Grande de Manatí', 'latitude': '18.2144', 'longitude': '-66.28665', 'sitecode': 'Rio_Grande_de_Manati', 'network': 'Para_La_Naturaleza', 'service': 'SOAP'}]
        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            sites = water.GetSites()
            variables = water.GetVariables()
            variables_to_filter = [variables[0]]
            sitesFiltered = water.GetSitesByVariable(variables_to_filter,sites)
        """
        sites = []
        new_sites = []

        if cookiCutter is not None:
            sites = cookiCutter
        else:
            sites = self.GetSites()

        for site in sites:
            site_desc = site['fullSiteCode']
            site_info = self.GetSiteInfo(site_desc)

            try:
                for variable_site in site_info['siteInfo']:
                    if variable_site['variableCode'] in specific_variables_codes:
                        new_sites.append(site)
                        break
            except Exception as ke:
                print(ke)
                print("site does not contain series")
        if format is "json":
            json_response = {}
            json_response['sites'] = sites
            return json_response

        elif format is "csv":
            df = pd.DataFrame.from_dict(new_sites)
            csv_sites = df.to_csv(index=False)
            # csv_sites.to_csv("/home/elkin/Projects/condaPackages/pywaterml/tests")
            return csv_sites
        else:
            return print("the only supported formats are json, csv, and waterml")

        return new_sites

    def GetInterpolation(self, GetValuesResponse, type= 'mean'):
        """
        Interpolates the data given by the GetValues function in order to fix datasets with missing values. Three ooptions for interpolation are offered:
        mean, backward, forward. The default is the mean interpolation.

        Args:

            GetValuesResponse: response from the GetValues() function
            type: type of interpolation to be performed: mean, backward, forward

        Returns:

            An object containing properties for the time series values for the given variable in the given site. The structure of the response is the following

                - variable: variable name
                - unit: units of the values
                - title: title of the time series values
                - values: an array of arrays containing [date, value]

            An example of the response is:
            {'variable': 'Water depth, averaged', 'unit': 'm', 'title': 'Water depth, averaged (m) vs Time', 'values': [['2013-08-03 05:00:00', 0.1815], ['2013-09-07 05:00:00', 0.187], ['2013-10-05 05:00:00', 0.226], ['2013-11-02 05:00:00', 0.1535], ['2013-12-07 05:00:00', 0.231], ['2014-01-11 05:00:00', 0.15525], ['2014-02-01 05:00:00', 0.124875], ['2014-03-01 05:00:00', 0.0], ['2014-04-05 05:00:00', 0.1145], ['2014-05-03 05:00:00', 0.0877], ['2014-06-07 05:00:00', 0.0], ['2014-07-05 05:00:00', 0.09375], ['2014-09-06 05:00:00', 0.12175], ['2014-10-04 05:00:00', 0.10325], ['2014-11-01 05:00:00', 0.1693], ['2014-12-06 05:00:00', 0.187], ['2015-01-03 05:00:00', 0.1285], ['2015-02-07 05:00:00', 0.125], ['2015-03-07 05:00:00', 0.159], ['2015-04-04 05:00:00', 0.14]]}
        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            sites = water.GetSites()
            firstSiteCode = sites[0]['sitecode']
            network = sites[0]['network']
            site_full_code = network +":"+firstSiteCode
            siteInfo = water.GetSiteInfo(site_full_code)
            firstVariableCode = siteInfo[0]['code']
            variable_full_code = network + ":" + firstVariableCode
            methodID = siteInfo[0]['methodID']
            start_date = siteInfo[0]['timeInterval']['beginDateTime'].split('T')[0]
            end_date = siteInfo[0]['timeInterval']['endDateTime'].split('T')[0]
            variableResponse= water.GetValues(site_full_code, variable_full_code, methodID, start_date, end_date)
            interpolationData = water.GetInterpolation(variableResponse, 'mean')
        """
        mean_interpolation = WaterAnalityca._Interpolate(GetValuesResponse)
        return mean_interpolation

    def GetMonthlyAverage(self, GetValuesResponse = None, site_full_code=None, variable_full_code =None, start_date=None, end_date=None, methodCode = None, qualityControlLevelCode = None):
        """
        Gets the monthly averages for a given variable, or from the response given by the GetValues function for a given site.

        Args:

            GetValuesResponse: response from the GetValues() function. If this is given the others paramters do not need to be given.
            site_full_code: A string representing the full code of the given site following the structure:
                -site_full_code = site network + ":" + site code
            variable_full_code: A string representing the full code of the given variable following the structure:
                -variable_full_code = site network + ":" + variable code
            methodID: method for data extraction for the given variable
            start_date: beginning date time for the time series of the variable
            end_date: end date time for the time series of the variable

        Returns:

            An object containing properties for the time series values for the given variable in the given site. The structure of the response is the following

                - variable: variable name
                - unit: units of the values
                - title: title of the time series values
                - values: an array of arrays containing [date, value]
        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            sites = water.GetSites()
            firstSiteCode = sites[0]['sitecode']
            network = sites[0]['network']
            site_full_code = network +":"+firstSiteCode
            siteInfo = water.GetSiteInfo(site_full_code)
            firstVariableCode = siteInfo[0]['code']
            variable_full_code = network + ":" + firstVariableCode
            methodID = siteInfo[0]['methodID']
            start_date = siteInfo[0]['timeInterval']['beginDateTime'].split('T')[0]
            end_date = siteInfo[0]['timeInterval']['endDateTime'].split('T')[0]
            variableResponse= water.GetValues(site_full_code, variable_full_code, methodID, start_date, end_date)
            monthly_averages = water.getMonthlyAverage(variableResponse)
        """
        if GetValuesResponse is not None:
            m_avg = WaterAnalityca._MonthlyAverages(GetValuesResponse)
            return m_avg
        else:
            vals = self.GetValues(site_full_code, variable_full_code,start_date, end_date, methodCode = methodCode, qualityControlLevelCode = qualityControlLevelCode)
            m_avg = WaterAnalityca._MonthlyAverages(vals)
            return m_avg

    def GetClustersMonthlyAvg(self,sites, variableCode, n_cluster = 3, methodCode = None, qualityControlLevelCode = None, timeUTC = False):
        """
        Gets "n" number of clusters using dtw time series interpolation for a given variable

        Args:

            sites: response from the GetSites() function. Performance of the fuction can be given if the resuls of the GetSitesByVariable() function is passed instead
            variableCode: string representing the variable code for the time series clusters of the given sites
            n_clusters: integer representing the number of cluster to form.

        Returns:

            An array of arrays of the following structure [monthly averages array, cluster_id]

            [[[0.141875, 0.1249375, 0.0795, 0.12725, 0.0877, 0.0, 0.09375, 0.1815, 0.15437499999999998, 0.164625, 0.1614, 0.20900000000000002], 1],
            [[0.1, 0.08662500000000001, 0.0414025, 0.048, 0.052, 0.0, 0.1105, 0.015, 0.06625, 0.10587500000000001, 0.0505, 0.046125], 0],
            [[0.2265, 0.27225, 0.17407499999999998, 0.13475, 0.14525, 0.129, 0.17825, 0.210625, 0.103125, 0.0, 0.23675], 2]]
        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            sites = water.GetSites()
            firstSiteCode = sites[0]['sitecode']
            network = sites[0]['network']
            site_full_code = network +":"+firstSiteCode
            siteInfo = water.GetSiteInfo(site_full_code)
            clusters = water.getClustersMonthlyAvg(sites,siteInfo[0]['name'])
        """
        timeseries = []
        timeSerie_cluster=[]
        try:
            for site in sites:
                # site_full_code = f'{site["network"]}:{site["sitecode"]}'
                site_full_code = site['fullSiteCode']
                try:
                    siteInfo =  self.GetSiteInfo(site_full_code)['siteInfo']
                    for sinfo in siteInfo:
                        if sinfo['variableCode'] == variableCode:
                            variable_full_code = sinfo['fullVariableCode']
                            start_date = sinfo['beginDateTime'].split('T')[0]
                            end_date = sinfo['endDateTime'].split('T')[0]

                            if timeUTC is True:
                                start_date = sinfo['beginDateTimeUTC'].split('T')[0]
                                end_date = sinfo['endDateTimeUTC'].split('T')[0]
                            variableResponse = self.GetValues(site_full_code, variable_full_code,start_date, end_date, methodCode= methodCode, qualityControlLevelCode=qualityControlLevelCode)
                            m_avg = self.GetMonthlyAverage(variableResponse)
                            timeseries.append(to_time_series(m_avg))
                            timeSerie_cluster.append([m_avg])
                            break
                except Exception as e:
                    print(e)
                    print("the current site does not contain siteInformation")
            formatted_time_series = to_time_series_dataset(timeseries)
            model = TimeSeriesKMeans(n_clusters = n_cluster, metric="dtw", max_iter=10)
            y_pred = model.fit_predict(formatted_time_series)
            for tc, y in zip(timeSerie_cluster,y_pred):
                tc.append(y)
            return timeSerie_cluster
        except KeyError as e:
            print(e)
            return timeSerie_cluster
        return timeSerie_cluster

if __name__ == "__main__":
    print("WaterML ops")

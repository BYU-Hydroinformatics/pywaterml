from suds.client import Client
import urllib.request
import urllib.error
import urllib.parse
import json
import xmltodict
from json import dumps, loads
from pywaterml.auxiliaryMod import Auxiliary, GetSoapsPlugin
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
        url: WaterOneFlow web service that complies to the SOAP protocol
    """
    def __init__(self,url = None):
        self.plugin = GetSoapsPlugin()
        self.url = url
        self.client = Client(url,plugins=[self.plugin], timeout= 500)
        self.aux = Auxiliary()

    def AddService(self,url):
        """
        Add a WaterOneFlow web service to the WaterMLOperations class. It can have any WaterOneFlow web service that uses the SOAP protocol.

        Args:
            url: WaterOneFlow web service that complies to the SOAP protocol
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
            print("There is already an enpoint, if you want to change the WaterOneFlow web service try ChangeEndpoint() function")
        pass

    def ChangeService(self,url):
        """
        Change the WaterOneFlow web service of a WaterMLOperations class. The current WaterOneFlow web service can be changed by any WaterOneFlow web service that uses the SOAP protocol.

        Args:
            url: WaterOneFlow web service that complies to the SOAP protocol

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
            print("There is no WaterOneFlow web service, please before changing an WaterOneFlow web service add one with AddEndpoint() function")
        pass

    def AvailableServices(self):
        """
        Give the WaterOneFlow web services that are available from a WaterOneFlow service containing a HIS catalog.

        Args:
            url: WaterOneFlow web service that complies to the SOAP protocol

        Returns:
            hs_services: available services in a given WaterOneFlow service containing a HIS catalog.

        Example::

            url_testing = "http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-country/hiscentral.asmx"
            water = WaterMLOperations(url = url_testing)
            available_services = water.AvailableServices(url_testing)
        """
        hs_services = {}
        if self.url:
            try:
                service_info = client.service.GetWaterOneFlowServiceInfo()
                services = service_info.ServiceInfo
                obj_services = self.aux._giveServices(services)
                hs_services['available'] = obj_services['working']
                hs_services['broken'] = obj_services['failed']
            except Exception as e:
                services = self.aux._parseService(self.url)
                # print(services)
                views = self.aux._giveServices(services)
                # print(views)
                hs_services['available'] = views['working']
                hs_services['broken'] = views['failed']
        return hs_services

    def GetWaterOneFlowServicesInfo(self):
        """
        Get all registered data services from a given WaterOneFlow Web service containing a HIS catalog. GetWaterOneFlowServiceInfo can be regarded as a special case of GetServicesInBox2, as the former requests the returns for the global area.
        Args:
            None

        Returns:
            A dictionary containing the following data for the different WaterOneFlow web services contained in the HIS catalog:
                - servURL: URL of the WaterOneFlow  web service
                - Title: title of the WaterOneFlow  web service
                - organization: supervising organization of the WaterOneFlow  web service
                - aabstract: abstract of the WaterOneFlow  web service

        Example::

            url_testing = "http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-country/hiscentral.asmx"
            water = WaterMLOperations(url = url_testing)
            services = water.GetWaterOneFlowServiceInfo()

        """
        try:
            service_info = client.service.GetWaterOneFlowServiceInfo()
            services = service_info.ServiceInfo
            return services
        except:
            services = self.aux._parseService(self.url)
            return services

    def GetSites(self, format="json"):
        """
        Get all the sites from a WaterOneFlow web service that complies to the SOAP protocol. The GetSites() function is similar to the GetSites() WaterML function.

        Args:
            format: format of the response (json, csv or waterML)

        Returns:
            A json, csv or waterML file containing the following data for all the differet sites:
                - latitude = The WGS84 latitude in decimal degrees
                - longitude = The WGS84 longitude in decimal degrees
                - site_name = The name of the site
                - network = Network that the site belongs to
                - sitecode = A short unique code of the site
                - siteID = The site ID in the original database
                - fullSiteCode = full site code of the current site. The fullSiteCode of every site is the following string: "network: sitecode"

        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            sites = water.GetSites()
        """
        try:
            sites = self.client.service.GetSites('[:]')
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
        except Exception as error:
            # print(error)
            sites_object={}
            if format is "waterml":
                return sites_object

            if format is "json":
                return sites_object
            elif format is "csv":
                df = pd.DataFrame.from_dict(sites_object)
                csv_sites = df.to_csv(index=False)
                # csv_sites.to_csv("/home/elkin/Projects/condaPackages/pywaterml/tests")
                return csv_sites

    def GetSitesByBoxObject(self,ext_list, inProjection, format="json"):
        """
        Get all the sites from a bounding box from a WaterOneFlow web service that complies to the SOAP protocol. The GetSitesByBoxObject() function is similar to the GetSitesByBoxObject() WaterML function.

        Args:
            ext_list: Array of bounding box coordinates in a given projection.
            inProjection: Projection from the array of coordinates of the given bounding box.
            format: format of the response (json, csv or waterML)

        Returns:
            A json, csv or waterML file containing the following data for all the differet sites in the selected boundingbox
                - latitude = The WGS84 latitude in decimal degrees
                - longitude = The WGS84 longitude in decimal degrees
                - site_name = The name of the site
                - network = Network that the site belongs to
                - sitecode = A short unique code of the site
                - siteID = The site ID in the original database
                - fullSiteCode = full site code of the current site. The fullSiteCode of every site is the following string: "network: sitecode"

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
            try:
                bbox = self.client.service.GetSitesByBoxObject(
                    x1, y1, x2, y2, '1', '')
            except Exception as error:
                print(e)
                raw_get = self.plugin.last_received_raw
                new_raws = raw_get.split(">")
                soap_namespace =  new_raws[1].split("xmlns")[1].split("=")[1]
                soap_namespace = soap_namespace.split('"')[1]
                version =  new_raws[0].split(" ")[1]
                binding.envns=('SOAP-ENV', soap_namespace)
                bbox = self.client.service.GetSitesByBoxObject(
                    x1, y1, x2, y2, '1', '')
                binding.envns=('SOAP-ENV', 'http://schemas.xmlsoap.org/soap/envelope/')
        except Exception as error:
            # print(error)
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
        Get variables meatada from a WaterOneFlow web service that complies to the SOAP protocol. GetVariables() function is similar to the GetVariables() WaterML function

        Args:
            format: format of the response (json, csv or waterML)
        Returns:
            A json, csv or waterML file containing the following data of the variables from the WaterOneFlow web service:

                - variableName: Name of the variable
                - unitName: Name of the units of the values associated to the given variable and site
                - unitAbbreviation: unit abbreviation of the units from the values associated to the given variable and site
                - noDataValue: value associated to lack of data.
                - isRegular: Boolean to indicate whether the observation measurements and collections regular
                - timeSupport: Boolean to indicate whether the values support time
                - timeUnitName: Time Units associated to the observation
                - timeUnitAbbreviation: Time units abbreviation
                - sampleMedium: the sample medium, for example water, atmosphere, soil.
                - speciation: The chemical sample speciation (as nitrogen, as phosphorus..)

        Example::
            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            variables = water.GetVariables()

        """
        return_array = []
        try:
            try:
                variables = self.client.service.GetVariables('[:]')
            except Exception as error:
                print(e)
                raw_get = self.plugin.last_received_raw
                new_raws = raw_get.split(">")
                soap_namespace =  new_raws[1].split("xmlns")[1].split("=")[1]
                soap_namespace = soap_namespace.split('"')[1]
                version =  new_raws[0].split(" ")[1]
                binding.envns=('SOAP-ENV', soap_namespace)
                variables = self.client.service.GetVariables('[:]')
                binding.envns=('SOAP-ENV', 'http://schemas.xmlsoap.org/soap/envelope/')
            if format is 'waterml':
                return variables
            variables_dict = xmltodict.parse(variables)
            variables_dict_object = json.dumps(variables_dict)

            variables_json = json.loads(variables_dict_object)
            array_variables = variables_json['variablesResponse']['variables']['variable']
            # print(array_variables)
            if isinstance(array_variables,type([])):
                for one_variable in array_variables:
                    return_object = {}
                    return_object = self.aux._getVariablesHelper(one_variable, return_object)
                    return_array.append(return_object)

            if isinstance(array_variables,dict):
                return_object = {}
                return_object = self.aux._getVariablesHelper(array_variables, return_object)
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
            format: format of the response (json, csv or waterML)

        Returns:

            A json, csv or waterML file containing the following data of the seleceted site from the WaterOneFlow web service:
                - siteName: Name of the site.
                - siteCode: Code of the site.
                - network: observation network that the site belongs to
                - fullVariableCode: The full variable code, for example: SNOTEL:SNWD.Use this value as the variableCode parameter in GetValues().
                - siteID: ID of the site
                - latitude: latitude of the site
                - longitude: longitude of the site
                - variableName: Name of the variable
                - unitName: Name of the units of the values associated to the given variable and site
                - unitAbbreviation: unit abbreviation of the units from the values associated to the given variable and site
                - dataType: Type of data
                - noDataValue: value associated to lack of data.
                - isRegular: Boolean to indicate whether the observation measurements and collections regular
                - timeSupport: Boolean to indicate whether the values support time
                - timeUnitName: Time Units associated to the observation
                - timeUnitAbbreviation: Time units abbreviation
                - sampleMedium: the sample medium, for example water, atmosphere, soil.
                - speciation: The chemical sample speciation (as nitrogen, as phosphorus..)
                - beginningDateTimeUTC: The UTC date and time of the first available
                - EndDateTimeUTC: The UTC date and time of the last available
                - beginningDateTime: The local date and time of the first available
                - EndDateTime: The local date and time of the last available
                - censorCode: The code for censored observations.  Possible values are nc (not censored), gt(greater than), lt (less than), nd (non-detect), pnq (present but not quantified)
                - methodCode: The code of the method or instrument used for the observation
                - methodID: The ID of the sensor or measurement method
                - qualityControlLevelCode: The code of the quality control level.  Possible values are -9999(Unknown), 0 (Raw data), 1 (Quality controlled data), 2 (Derived products), 3 (Interpretedproducts), 4 (Knowledge products)
                - qualityControlLevelID: The ID of the quality control level. Usually 0 means raw data and 1 means quality controlled data.
                - sourceCode: The code of the data source.
                - timeOffSet: The difference between local time and UTC time in hours.

        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            sites = water.GetSites()
            firstSiteFullSiteCode = sites[0]['fullSiteCode']
            siteInfo = water.GetSiteInfo(firstSiteFullSiteCode)
        """
        try:
            site_info_Mc = self.client.service.GetSiteInfo(site_full_code)
        except Exception as error:
            print(error)
            raw_get = self.plugin.last_received_raw
            new_raws = raw_get.split(">")
            soap_namespace =  new_raws[1].split("xmlns")[1].split("=")[1]
            soap_namespace = soap_namespace.split('"')[1]
            version =  new_raws[0].split(" ")[1]
            binding.envns=('SOAP-ENV', soap_namespace)
            site_info_Mc = self.client.service.GetSiteInfo(site_full_code)
            binding.envns=('SOAP-ENV', 'http://schemas.xmlsoap.org/soap/envelope/')

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
            # print(ke)
            # print("No series for the site")
            return_array = []
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
            # return return_array
        return return_array

    def GetValues(self,site_full_code, variable_full_code, start_date, end_date, methodCode = None, qualityControlLevelCode = None, format = 'json'):
        """
        Get the specific values for an specific variable in a site. GetValues() function is similar to the GetValues() WaterML function.

        Args:
            site_full_code: A string representing the full code of the given site following the structure
                - site_full_code = site network + ":" + site code
            variable_full_code: A string representing the full code of the given variable following the structure
                - variable_full_code = site network + ":" + variable code
            start_date: beginning date time for the time series of the variable
            end_date: end date time for the time series of the variable
            methodCode: method code for data extraction for the given variable
            qualityControlLevelCode: The ID of the quality control level.Typically 0 is used for raw dataand 1 is used for quality controlled data.To get a list of possible quality controllevel IDs,
                see qualityControlLevelCode column in the output of GetSiteInfo(). If qualityControlLevelCode is not specified,then the observations in the output data.frame won’t befiltered
                by quality control level code.
            format: format of the response (json, csv or waterML)

        Returns:
            An object containing properties for the time series values for the given variable in the given site. The object has the following data:
                - siteName: Name of the site.
                - siteCode: Code of the site.
                - network: observation network that the site belongs to
                - siteID: ID of the site
                - latitude: latitude of the site
                - longitude: longitude of the site
                - variableName: Name of the variable
                - unitName: Name of the units of the values associated to the given variable and site
                - unitAbbreviation: unit abbreviation of the units from the values associated to the given variable and site
                - dataType: Type of data
                - noDataValue: value associated to lack of data.
                - isRegular: Boolean to indicate whether the observation measurements and collections regular
                - timeSupport: Boolean to indicate whether the values support time
                - timeUnitName: Time Units associated to the observation
                - timeUnitAbbreviation: Time units abbreviation
                - sampleMedium: the sample medium, for example water, atmosphere, soil.
                - speciation: The chemical sample speciation (as nitrogen, as phosphorus..)
                - dateTimeUTC: The UTC time of the observation.
                - dateTime: The local date/time of the observation.
                - dataValue: Data value from the observation.
                - censorCode: The code for censored observations.  Possible values are nc (not censored), gt(greater than), lt (less than), nd (non-detect), pnq (present but not quantified)
                - methodCode: The code of the method or instrument used for the observation
                - qualityControlLevelCode: The code of the quality control level.  Possible values are -9999(Unknown), 0 (Raw data), 1 (Quality controlled data), 2 (Derived products), 3 (Interpretedproducts), 4 (Knowledge products)
                - sourceCode: The code of the data source
                - timeOffSet: The difference between local time and UTC time in hours.

        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            sites = water.GetSites()
            firstSiteFullSiteCode = sites[0]['fullSiteCode']
            siteInfo = water.GetSiteInfo(firstSiteFullSiteCode)
            firstVariableFullCode = siteInfo['siteInfo'][0]['fullVariableCode']
            start_date = siteInfo['siteInfo'][0]['beginDateTime'].split('T')[0]
            end_date = siteInfo['siteInfo'][0]['endDateTime'].split('T')[0]
            variableResponse= water.GetValues(site_full_code, variable_full_code, start_date, end_date)
        """
        try:
            values = self.client.service.GetValues(site_full_code, variable_full_code, start_date, end_date, "")
        except Exception as error:
            print(error)
            raw_get = self.plugin.last_received_raw
            new_raws = raw_get.split(">")
            soap_namespace =  new_raws[1].split("xmlns")[1].split("=")[1]
            soap_namespace = soap_namespace.split('"')[1]
            version =  new_raws[0].split(" ")[1]
            binding.envns=('SOAP-ENV', soap_namespace)
            values = self.client.service.GetValues(site_full_code, variable_full_code, start_date, end_date, "")
            binding.envns=('SOAP-ENV', 'http://schemas.xmlsoap.org/soap/envelope/')
        if format is "waterml":
            return values
        values_dict = xmltodict.parse(values)
        values_json_object = json.dumps(values_dict)
        # print(values_json_object)

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
                                        # print(ke)
                                        # print(times_series)
                                        json_response = self.aux._getValuesHelper2(times_series,json_response)
                                        # print(json_response)
                                        json_response = self.aux._getValuesHelper(k,json_response)
                                        return_array.append(json_response)
                                        json_response = {}

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
            # print(error)

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
        Get the specific sites according to a variable search array from a WaterOneFlow web service that complies to the SOAP protocol. The GetSitesByVariable() is an addition to the WaterML functions
        because it allows the user to retrieve sites that contains the epecific site/s.

        Args

            specific_variables: An array of strings representing a list of variables that will serve as a filter when retrieving sites.
            cookiCutter: A list containing the different information from each site. It can be the response of the GetSites() or GetSitesByBoxObject() functions.
            if the cookiCutter is not specified, the function will filter all the functions calling GetSites() internally.
            format: format of the response (json, csv or waterML)

        Returns:

            An array of objects that represent each site. The structure of the response is the following:

                - latitude = The WGS84 latitude in decimal degrees
                - longitude = The WGS84 longitude in decimal degrees
                - site_name = The name of the site
                - network = Network that the site belongs to
                - sitecode = A short unique code of the site
                - siteID = The site ID in the original database
                - fullSiteCode = full site code of the current site. The fullSiteCode of every site is the following string: "network: sitecode"

        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            sites = water.GetSites()['sites']
            variables = water.GetVariables()['variables']

            # choose the first variable to filter#

            variables_to_filter = [variables[0][variableCode]]
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
                    # print(variable_site['variableCode'],specific_variables_codes )
                    if variable_site['variableCode'] in specific_variables_codes:
                        new_sites.append(site)
                        # print(new_sites)
                        break
            except Exception as ke:
                if format is "json":
                    json_response = {}
                    json_response['sites'] = new_sites
                    return json_response

                elif format is "csv":
                    df = pd.DataFrame.from_dict(new_sites)
                    csv_sites = df.to_csv(index=False)
                    # csv_sites.to_csv("/home/elkin/Projects/condaPackages/pywaterml/tests")
                    return csv_sites
                else:
                    return print("the only supported formats are json, csv, and waterml")
                # print(ke)
                # print("site does not contain series")
        if format is "json":
            json_response = {}
            json_response['sites'] = new_sites
            # print(json_response)
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
            format: format of the response (json, csv or waterML)

        Returns:

            An array containing the interpolation chosen by the user (backward, mean, forward)

        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            sites = water.GetSites()
            firstSiteFullSiteCode = sites[0]['fullSiteCode']
            siteInfo = water.GetSiteInfo(firstSiteFullSiteCode)
            firstVariableFullCode = siteInfo['siteInfo'][0]['fullVariableCode']
            start_date = siteInfo['siteInfo'][0]['beginDateTime'].split('T')[0]
            end_date = siteInfo['siteInfo'][0]['endDateTime'].split('T')[0]
            variableResponse= water.GetValues(site_full_code, variable_full_code, start_date, end_date)
            interpolationData = water.GetInterpolation(variableResponse, 'mean')
        """
        mean_interpolation = WaterAnalityca._Interpolate(GetValuesResponse)
        return mean_interpolation

    def GetMonthlyAverage(self, GetValuesResponse = None, site_full_code=None, variable_full_code =None, start_date=None, end_date=None, methodCode = None, qualityControlLevelCode = None):
        """
        Gets the monthly averages for a given variable, or from the response given by the GetValues function for a given site.

        Args:

            GetValuesResponse: response from the GetValues() function. If this is given the others paramters do not need to be given.
            site_full_code: A string representing the full code of the given site following the structure
                - site_full_code = site network + ":" + site code
            variable_full_code: A string representing the full code of the given variable following the structure
                - variable_full_code = site network + ":" + variable code
            start_date: beginning date time for the time series of the variable
            end_date: end date time for the time series of the variable
            methodCode: method code for data extraction for the given variable
            qualityControlLevelCode: The ID of the quality control level.Typically 0 is used for raw dataand 1 is used for quality controlled data.
                To get a list of possible quality controllevel IDs, see qualityControlLevelCode column in the output of GetSiteInfo().
                If qualityControlLevelCode is not specified,then the observations in the output data.frame won’t befiltered by quality control level code.


        Returns:

            An object containing properties for the time series values for the given variable in the given site. The structure of the response is the following

                - variable: variable name
                - unit: units of the values
                - title: title of the time series values
                - values: an array of arrays containing [date, value]
        Example::

            water = WaterMLOperations(url = url_testing)
            sites = water.GetSites()
            firstSiteFullSiteCode = sites[0]['fullSiteCode']
            siteInfo = water.GetSiteInfo(firstSiteFullSiteCode)
            firstVariableFullCode = siteInfo['siteInfo'][0]['fullVariableCode']
            start_date = siteInfo['siteInfo'][0]['beginDateTime'].split('T')[0]
            end_date = siteInfo['siteInfo'][0]['endDateTime'].split('T')[0]
            variableResponse= water.GetValues(site_full_code, variable_full_code, start_date, end_date)
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

            sites: response from the GetSites() function. Performance of the fuction can be given if the resuls of the GetSitesByVariable() function is passed instead.
            variableCode: string representing the variable code for the time series clusters of the given sites.
            n_clusters: integer representing the number of cluster to form.
            methodCode: method code for data extraction for the given variable.
            qualityControlLevelCode: The ID of the quality control level.Typically 0 is used for raw dataand 1 is used for quality controlled data.
                To get a list of possible quality controllevel IDs, see qualityControlLevelCode column in the output of GetSiteInfo(). If qualityControlLevelCode is not specified,
                then the observations in the output data.frame won’t befiltered by quality control level code.
            timeUTC: Boolean to use the UTC time instead of the time of the observation.
        Returns:

            An array of arrays of the following structure [monthly averages array, cluster_id]

            [[[0.141875, 0.1249375, 0.0795, 0.12725, 0.0877, 0.0, 0.09375, 0.1815, 0.15437499999999998, 0.164625, 0.1614, 0.20900000000000002], 1],
            [[0.1, 0.08662500000000001, 0.0414025, 0.048, 0.052, 0.0, 0.1105, 0.015, 0.06625, 0.10587500000000001, 0.0505, 0.046125], 0],
            [[0.2265, 0.27225, 0.17407499999999998, 0.13475, 0.14525, 0.129, 0.17825, 0.210625, 0.103125, 0.0, 0.23675], 2]]
        Example::

            url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
            water = WaterMLOperations(url = url_testing)
            sites = water.GetSites()
            firstSiteFullSiteCode = sites[0]['fullSiteCode']
            siteInfo = water.GetSiteInfo(firstSiteFullSiteCode)['siteInfo']
            clusters = water.getClustersMonthlyAvg(sites,siteInfo[0]['variableCode'])
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
            # print(e)
            return timeSerie_cluster
        return timeSerie_cluster

if __name__ == "__main__":
    print("WaterML ops")

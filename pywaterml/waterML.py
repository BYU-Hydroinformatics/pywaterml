from suds.client import Client  # For parsing WaterML/XML
import json
import xmltodict
from json import dumps, loads
from pywaterml.aux import Auxiliary
from pywaterml.analyzeData import WaterAnalityca
from pyproj import Proj, transform  # Reprojecting/Transforming coordinates
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
from tslearn.metrics import dtw
from tslearn.clustering import TimeSeriesKMeans
from tslearn.utils import to_time_series, to_time_series_dataset

class WaterMLOperations():
    def __init__(self,url = None):
        self.url = url
        self.client = Client(url, timeout= 500)
        self.aux = Auxiliary()
    """
        Function to add a endpoint if needed
        AddEndpoint()
    """
    def AddEndpoint(self,url):
        if self.url is None:
            self.url = url
            self.client = Client(url, timeout= 500)
        else:
            print("There is already an enpoint, if you want to change the endpoint try ChangeEndpoint() function")
        pass
    """
        Function to change the endpoint if needed
        ChangeEndpoint()
    """
    def ChangeEndpoint(self,url):
        if self.url is not None:
            self.url = url
            self.client = Client(url, timeout= 500)
        else:
            print("There is no endpoint, please before changing an endpoint add one with AddEndpoint() function")
        pass

    """
        Get all the sites from a endpoint
        GetSites() function is similar to the
        GetSites() WaterML function
    """
    def GetSites(self):
        # True Extent is on and necessary if the user is trying to add USGS or
        # Get a list of all the sites and their respective lat lon.

        sites = self.client.service.GetSites('[:]')
        sites_json={}
        if isinstance(sites, str):
            sites_dict = xmltodict.parse(sites)
            sites_json_object = json.dumps(sites_dict)
            sites_json = json.loads(sites_json_object)
        else:
            sites_json_object = suds_to_json(sites)
            sites_json = json.loads(sites_json_object)

        sites_object = Auxiliary.parseJSON(sites_json)

        return sites_object

    """
        Get all the sites from a selected biding box
        GetSitesByBoxObject() function is similar to the
        GetSitesByBoxObject() WaterML function
    """
    def GetSitesByBoxObject(self,ext_list,inProjection):
        # return_obj['level'] = extent_value
        # Reprojecting the coordinates from 3857 to 4326 using pyproj
        # inProj = Proj(init='epsg:3857')
        inProj = Proj(init=inProjection)
        outProj = Proj(init='epsg:4326')

        minx, miny = ext_list[0], ext_list[1]
        maxx, maxy = ext_list[2], ext_list[3]
        x1, y1 = transform(inProj, outProj, minx, miny)
        x2, y2 = transform(inProj, outProj, maxx, maxy)
        bbox = self.client.service.GetSitesByBoxObject(
            x1, y1, x2, y2, '1', '')
        # Get Sites by bounding box using suds
        # Creating a sites object from the endpoint. This site object will
        # be used to generate the geoserver layer. See utilities.py.
        wml_sites = self.aux.parseWML(bbox)
        # wml_sites = xmltodict.parse(bbox)
        sites_parsed_json = json.dumps(wml_sites)

        return sites_parsed_json
    """
        Get all the variables from an endpoint
        GetVariables() function is similar to the
        GetVariables() WaterML function
    """
    def GetVariables(self):
      variables = self.client.service.GetVariables('[:]')

      variables_dict = xmltodict.parse(variables)
      variables_dict_object = json.dumps(variables_dict)

      variables_json = json.loads(variables_dict_object)
      array_variables = variables_json['variablesResponse']['variables']['variable']
      array_final_variables = []

      if isinstance(array_variables,type([])):
          for one_variable in array_variables:
              array_final_variables.append(one_variable['variableName'])

      if isinstance(array_variables,dict):
          array_final_variables.append(array_variables['variableName'])

      return array_final_variables
    """
        Get the information from a site.
        GetSiteInfo() function is similar to the
        GetSiteInfo() WaterML function
    """
    def GetSiteInfo(self,site_full_code):

        site_info_Mc = self.client.service.GetSiteInfo(site_full_code)
        site_info_Mc_dict = xmltodict.parse(site_info_Mc)
        site_info_Mc_json_object = json.dumps(site_info_Mc_dict)
        site_info_Mc_json = json.loads(site_info_Mc_json_object)
        try:
            object_methods = site_info_Mc_json['sitesResponse']['site']['seriesCatalog']['series']

            return_aray = []
            if(isinstance(object_methods,(dict))):
                return_obj = {}
                return_obj['name'] = object_methods['variable']['variableName']
                return_obj['code'] = object_methods['variable']['variableCode']['#text']
                return_obj['count'] = object_methods['valueCount']
                if 'method' in object_methods:
                    return_obj['methodID'] = object_methods['method']['@methodID']
                else:
                    return_obj['methodID'] = None
                return_obj['description'] = object_methods['source']
                return_obj['timeInterval'] = object_methods['variableTimeInterval']
                return_aray.append(return_obj)
                return return_aray

            else:
                for object_method in object_methods:
                    return_obj = {}
                    return_obj['name'] = object_method['variable']['variableName']
                    return_obj['code'] = object_method['variable']['variableCode']['#text']
                    return_obj['count'] = object_method['valueCount']
                    if 'method' in object_method:
                        return_obj['methodID'] = object_method['method']['@methodID']
                    else:
                        return_obj['methodID'] = None
                    return_obj['description'] = object_method['source']
                    return_obj['timeInterval'] = object_method['variableTimeInterval']
                    return_aray.append(return_obj)
                    return return_aray

        except KeyError:
            print("No series for the site")
            return_aray = []
            return return_aray
        return return_aray
    """
        Get the specific values for an specific variable in a site.
        GetValues() function is similar to the
        GetValues() WaterML function
    """
    def GetValues(self,site_full_code, variable_full_code, methodID, start_date, end_date):

        values = self.client.service.GetValues(
            site_full_code, variable_full_code, start_date, end_date, "")
        values_dict = xmltodict.parse(values)  # Converting xml to dict
        values_json_object = json.dumps(values_dict)
        values_json = json.loads(values_json_object)
        times_series = {}
        if 'timeSeriesResponse' in values_json:

            times_series = values_json['timeSeriesResponse'][
                'timeSeries']  # Timeseries object for the variable
            if times_series['values'] is not None:

                graph_json = {}  # json object that will be returned to the front end
                graph_json["variable"] = times_series['variable']['variableName']
                graph_json["unit"]=""
                if times_series['variable']['unit']['unitAbbreviation'] is not None:
                    graph_json["unit"] = times_series[
                        'variable']['unit']['unitAbbreviation']

                graph_json["title"] = times_series['variable']['variableName'] + " (" + graph_json["unit"] + ") vs Time"
                for j in times_series['values']:  # Parsing the timeseries
                    data_values = []
                    if j == "value":
                        if type(times_series['values']['value']) is list:

                            for k in times_series['values']['value']:
                                # return_obj['k']= k

                                try:
                                    if k['@methodCode'] == methodID:
                                        time = k['@dateTimeUTC']
                                        time1 = time.replace("T", "-")
                                        time_split = time1.split("-")
                                        year = int(time_split[0])
                                        month = int(time_split[1])
                                        day = int(time_split[2])
                                        hour_minute = time_split[3].split(":")
                                        hour = int(hour_minute[0])
                                        minute = int(hour_minute[1])
                                        value = float(str(k['#text']))
                                        date_string = datetime(
                                            year, month, day, hour, minute)
                                        date_string_converted = date_string.strftime("%Y-%m-%d %H:%M:%S")
                                        data_values.append([date_string_converted,value])
                                        data_values.sort()
                                    graph_json["values"] = data_values
                                except KeyError:  # The Key Error kicks in when there is only one timeseries
                                    time = k['@dateTimeUTC']
                                    time1 = time.replace("T", "-")
                                    time_split = time1.split("-")
                                    year = int(time_split[0])
                                    month = int(time_split[1])
                                    day = int(time_split[2])
                                    hour_minute = time_split[3].split(":")
                                    hour = int(hour_minute[0])
                                    minute = int(hour_minute[1])
                                    value = float(str(k['#text']))
                                    date_string = datetime(
                                        year, month, day, hour, minute)
                                    data_values.append([date_string,value])
                                    data_values.sort()
                                graph_json["values"] = data_values
                                # return_obj['graphs']= graph_json

                        else:  # The else statement is executed is there is only one value in the timeseries
                            try:
                                if times_series['values']['value']['@methodCode'] == methodID:
                                    time = times_series['values'][
                                        'value']['@dateTimeUTC']
                                    time1 = time.replace("T", "-")
                                    time_split = time1.split("-")
                                    year = int(time_split[0])
                                    month = int(time_split[1])
                                    day = int(time_split[2])
                                    hour_minute = time_split[3].split(":")
                                    hour = int(hour_minute[0])
                                    minute = int(hour_minute[1])
                                    value = float(
                                        str(times_series['values']['value']['#text']))

                                    date_string = datetime(
                                        year, month, day, hour, minute)

                                    data_values.append([date_string,value])
                                    data_values.sort()
                                    graph_json["values"] = data_values
                                    # return_obj['graphs']=graph_json

                            except KeyError:
                                time = times_series['values'][
                                    'value']['@dateTimeUTC']
                                time1 = time.replace("T", "-")
                                time_split = time1.split("-")
                                year = int(time_split[0])
                                month = int(time_split[1])
                                day = int(time_split[2])
                                hour_minute = time_split[3].split(":")
                                hour = int(hour_minute[0])
                                minute = int(hour_minute[1])
                                value = float(
                                    str(times_series['values']['value']['#text']))
                                date_string = datetime(
                                    year, month, day, hour, minute)
                                data_values.append([date_string,value])
                                data_values.sort()
                                graph_json["values"] = data_values
                                # return_obj['graphs']=graph_json
        # return return_obj
        return graph_json

    """
        Get the specific sites according to a keyword search array.
        GetSitesByVariable()
    """
    def GetSitesByVariable(self,specific_variables,cookiCutter = None):

        sites = []
        new_sites = []

        if cookiCutter is not None:
            sites = cookiCutter
        else:
            sites = self.GetSites()

        for site in sites:
            site_obj = {}
            sitecode = site['sitecode']
            site_name = site['sitename']
            network = site["network"]
            site_obj['sitecode'] = sitecode
            site_obj['sitename'] = site_name
            site_obj['network'] = network
            site_obj['latitude'] = site['latitude']
            site_obj['longitude'] = site['longitude']

            site_desc = network + ":" + sitecode
            site_info = self.GetSiteInfo(site_desc)

            for variable_site in site_info:
                if variable_site['name'] in specific_variables:
                    new_sites.append(site_obj)
                    break

        return new_sites

    """
        Return the mean interpolation for the GetValues()
    """
    def Interpolate(self, GetValuesResponse, type= 'mean'):
        mean_interpolation = WaterAnalityca.Interpolate(GetValuesResponse)
        return mean_interpolation
    """
        Return the monthly averages for a variable

    """
    def getMonthlyAverage(self, GetValuesResponse = None, site_full_code=None, variable_full_code=None, methodID=None, start_date=None, end_date=None):
        if GetValuesResponse is not None:
            m_avg = WaterAnalityca.MonthlyAverages(GetValuesResponse)
            return m_avg
        else:
            vals = self.GetValues(site_full_code, variable_full_code, methodID, start_date, end_date)
            m_avg = WaterAnalityca.MonthlyAverages(vals)
            return m_avg
    def getClustersMonthlyAvg(self,sites, variable, n_cluster = 3):
        timeseries = []
        i = 0
        for site in sites:
            print(i)
            site_full_code = f'{site["network"]}:{site["sitecode"]}'
            siteInfo =  self.GetSiteInfo(site_full_code)
            for sinfo in siteInfo:
                if sinfo['name'] == variable:
                    firstVariableCode = siteInfo[0]['code']
                    variable_full_code = site["network"] + ":" + firstVariableCode
                    methodID = siteInfo[0]['methodID']
                    start_date = siteInfo[0]['timeInterval']['beginDateTime'].split('T')[0]
                    end_date = siteInfo[0]['timeInterval']['endDateTime'].split('T')[0]
                    variableResponse = self.GetValues(site_full_code, variable_full_code, methodID, start_date, end_date)
                    m_avg = self.getMonthlyAverage(variableResponse)
                    timeseries.append(to_time_series(m_avg))
                    break
            i = i + 1
        # X = np.array(np.array(list2))
        formatted_time_series = to_time_series_dataset(timeseries)
        # print(X)
        model = TimeSeriesKMeans(n_clusters = n_cluster, metric="dtw", max_iter=10)
        y_pred = model.fit_predict(formatted_time_series)
        return y_pred
if __name__ == "__main__":
    print("WaterML ops")

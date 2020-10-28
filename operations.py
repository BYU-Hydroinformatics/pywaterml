from suds.client import Client  # For parsing WaterML/XML
import json
import xmltodict
from json import dumps, loads
from aux import Auxiliary
from pyproj import Proj, transform  # Reprojecting/Transforming coordinates
import xml.etree.ElementTree as ET

class WaterMLOperations(url):

    """
        Get all the sites from a endpoint
        GetSites() function is similar to the
        GetSites() WaterML function
    """
    client = Client(url, timeout= 500)

    def GetSites():
        # True Extent is on and necessary if the user is trying to add USGS or
        # Get a list of all the sites and their respective lat lon.
        
        sites = client.service.GetSites('[:]')
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
    def GetSitesByBoxObject(ext_list):
        return_obj['level'] = extent_value
        # Reprojecting the coordinates from 3857 to 4326 using pyproj
        inProj = Proj(init='epsg:3857')
        outProj = Proj(init='epsg:4326')
        minx, miny = ext_list[0], ext_list[1]
        maxx, maxy = ext_list[2], ext_list[3]
        x1, y1 = transform(inProj, outProj, minx, miny)
        x2, y2 = transform(inProj, outProj, maxx, maxy)
        bbox = client.service.GetSitesByBoxObject(
            x1, y1, x2, y2, '1', '')
        # Get Sites by bounding box using suds
        # Creating a sites object from the endpoint. This site object will
        # be used to generate the geoserver layer. See utilities.py.
        wml_sites = Auxiliary.parseWML(bbox)
        # wml_sites = xmltodict.parse(bbox)
        sites_parsed_json = json.dumps(wml_sites)

        return sites_parsed_json
    """
        Get all the sites from a selected biding box
        GetSitesByBoxObject() function is similar to the
        GetSitesByBoxObject() WaterML function
    """
    def GetVariables():
      variables = client.service.GetVariables('[:]')

      variables_dict = xmltodict.parse(keywords)
      variables_dict_object = json.dumps(keywords_dict)

      variables_json = json.loads(variables_dict_object)
      array_variables = variables_json['variablesResponse']['variables']['variable']
      array_final_variables = []

      if isinstance(array_variables,type([])):
          for one_variable in array_variables:
              array_final_variables.append(one_variable['variableName'])

      if isinstance(array_variables,dict):
          array_final_variables.append(array_variables['variableName'])

      return array_final_variables

if __name__ == "__main__":
    print("WaterML ops")

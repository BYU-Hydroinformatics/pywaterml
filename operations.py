from suds.client import Client  # For parsing WaterML/XML
import json
from json import dumps, loads
from aux import Auxiliary
from pyproj import Proj, transform  # Reprojecting/Transforming coordinates

class WaterMLOperations():

    """
        Get all the sites from a endpoint
        GetSites() function is similar to the
        GetSites() WaterML function
    """
    def GetSites(url):
        client = Client(url, timeout= 500)
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
    def GetSitesByBoxObject(url, ext_list):
        client = Client(url, timeout= 500)
        extent_value = request.POST['extent_val']
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

if __name__ == "__main__":
    print("WaterML ops")

import requests
import json
from suds.sudsobject import asdict


class Auxiliary():
    """
    This class represents the Auxiliary object for the WaterMLOperations class. The Auxiliary provides functions related to parsing data from XML
    to JSON format, and the creation of JSON responses to have a more digested output. However, this is a helper class for the main WaterMLOperations
    class.
    """
    def _parseJSON(json):
        """
        Helper function to parse JSON data into a python dictionary. It is used in the WaterMLOperations GetSites() function.
        Args:
            json: json object
        Returns:
            hs_sites: Dictionary from all the sites of an specific URL
        """
        hs_sites = []
        sites_object = None
        try:
            if "sitesResponse" in json:
                sites_object = json['sitesResponse']['site']
                if type(sites_object) is list:
                    for site in sites_object:
                        hs_json = {}
                        latitude = site['siteInfo']['geoLocation'][
                            'geogLocation']['latitude']
                        longitude = site['siteInfo']['geoLocation'][
                            'geogLocation']['longitude']
                        site_name = site['siteInfo']['siteName']
                        site_name = site_name.encode("utf-8")
                        network = site['siteInfo']['siteCode']["@network"]
                        sitecode = site['siteInfo']['siteCode']["#text"]
                        siteID = site['siteInfo']['siteCode']["@siteID"]
                        hs_json["sitename"] = site_name.decode("UTF-8")
                        hs_json["latitude"] = latitude
                        hs_json["longitude"] = longitude
                        hs_json["sitecode"] = sitecode
                        hs_json["network"] = network
                        hs_json["fullSiteCode"] = network +":" + sitecode
                        hs_json["siteID"] = siteID
                        # hs_json["service"] = "SOAP"
                        hs_sites.append(hs_json)
                else:
                    hs_json = {}
                    latitude = sites_object['siteInfo'][
                        'geoLocation']['geogLocation']['latitude']
                    longitude = sites_object['siteInfo'][
                        'geoLocation']['geogLocation']['longitude']
                    site_name = sites_object['siteInfo']['siteName']
                    site_name = site_name.encode("utf-8")
                    network = sites_object['siteInfo']['siteCode']["@network"]
                    sitecode = sites_object['siteInfo']['siteCode']["#text"]
                    siteID = sites_object['siteInfo']['siteCode']["@siteID"]
                    hs_json["sitename"] = site_name.decode("UTF-8")
                    hs_json["latitude"] = latitude
                    hs_json["longitude"] = longitude
                    hs_json["sitecode"] = sitecode
                    hs_json["network"] = network
                    hs_json["fullSiteCode"] = network +":" + sitecode
                    hs_json["siteID"] = siteID
                    # hs_json["service"] = "SOAP"
                    hs_sites.append(hs_json)
        except (ValueError, KeyError) as error:
            print("There is a discrepancy in the structure of the response. It is possible that the respond object does not contain the sitesResponse attribute")
            print(error)
        return hs_sites

    def _parseWML(self,bbox):
        """
        Helper function to parse JSON data from a bounding box into a python dictionary . It is used in the WaterMLOperations GetSitesByBoxObject() function.
        Args:
            bbox: json object from belonging to the bounding box
        Returns:
            hs_sites: Dictionary from all the sites of an specific URL
        """
        hs_sites = []

        bbox_json = self._recursive_asdict(bbox)
        try:
            if type(bbox_json['site']) is list:
                for site in bbox_json['site']:
                    hs_json = {}
                    site_name = site['siteInfo']['siteName']
                    latitude = site['siteInfo']['geoLocation'][
                        'geogLocation']['latitude']
                    longitude = site['siteInfo']['geoLocation'][
                        'geogLocation']['longitude']
                    network = site['siteInfo']['siteCode'][0]['_network']
                    sitecode = site['siteInfo']['siteCode'][0]['value']
                    siteID = site['siteInfo']['siteCode'][0]["siteID"]
                    hs_json["sitename"] = site_name
                    hs_json["latitude"] = latitude
                    hs_json["longitude"] = longitude
                    hs_json["sitecode"] = sitecode
                    hs_json["network"] = network
                    hs_json["siteID"] = siteID

                    # hs_json["service"] = "SOAP"
                    hs_sites.append(hs_json)
            else:
                hs_json = {}
                site_name = bbox_json['site']['siteInfo']['siteName']
                latitude = bbox_json['site']['siteInfo'][
                    'geoLocation']['geogLocation']['latitude']
                longitude = bbox_json['site']['siteInfo'][
                    'geoLocation']['geogLocation']['longitude']
                network = bbox_json['site']['siteInfo']['siteCode'][0]['_network']
                sitecode = bbox_json['site']['siteInfo']['siteCode'][0]['value']
                siteID = bbox_json['site']['siteInfo']['siteCode'][0]["siteID"]

                hs_json["sitename"] = site_name
                hs_json["latitude"] = latitude
                hs_json["longitude"] = longitude
                hs_json["sitecode"] = sitecode
                hs_json["network"] = network
                hs_json["siteID"] = siteID
                # hs_json["service"] = "SOAP"
                hs_sites.append(hs_json)
        except (AssertionError, KeyError) as error:
            print("There is an error while parsing the response object ", error)

        return hs_sites

    def _recursive_asdict(self,d):
        """
        Helper function to make Suds object into serializable format recurvesively . It is used in the _parseJSON and _parseWML functions.
        Args:
            d: json object
        Returns:
            None
        """
        out = {}
        try:
            for k, v in asdict(d).items():
                if hasattr(v, "__keylist__"):
                    out[k] = self._recursive_asdict(v)
                elif isinstance(v, list):
                    out[k] = []
                    for item in v:
                        if hasattr(item, "__keylist__"):
                            out[k].append(self._recursive_asdict(item))
                        else:
                            out[k].append(item)
                else:
                    out[k] = v
        except AssertionError as error:
            print("The following Suds Object cannot be converted to serializable object", error)
        return out

if __name__ == "__main__":
    print("Why are you running the wrapper class file?")

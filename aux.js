import requests
import json

class Auxiliary():
    def parseJSON(json):
        hs_sites = []
        sites_object = None
        try:
            if "sitesResponse" in json:
                sites_object = json['sitesResponse']['site']
                # If statement is executed for multiple sites within the HydroServer, if there is a single site then it goes to the else statement
                # Parse through the HydroServer and each site with its metadata as a
                # dictionary object to the hs_sites list
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

                        hs_json["sitename"] = site_name.decode("UTF-8")
                        hs_json["latitude"] = latitude
                        hs_json["longitude"] = longitude
                        hs_json["sitecode"] = sitecode
                        hs_json["network"] = network
                        hs_json["service"] = "SOAP"
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

                    hs_json["sitename"] = site_name.decode("UTF-8")
                    hs_json["latitude"] = latitude
                    hs_json["longitude"] = longitude
                    hs_json["sitecode"] = sitecode
                    hs_json["network"] = network
                    hs_json["service"] = "SOAP"
                    hs_sites.append(hs_json)
        except ValueError:
            print("There is a discrepancy in the structure of the response. It is possible that the respond object does not contain the sitesResponse attribute")

        return hs_sites

    def parseWML(bbox):
        hs_sites = []
        # print bbox

        bbox_json = recursive_asdict(bbox)  # Convert bounding box to json

        # If there are multiple sites, create a list of of dictionaries with
        # metadata
        try:
            if type(bbox_json['site']) is list:
                for site in bbox_json['site']:
                    hs_json = {}
                    site_name = site['siteInfo']['siteName']
                    # site_name = site_name.encode("utf-8")
                    latitude = site['siteInfo']['geoLocation'][
                        'geogLocation']['latitude']
                    longitude = site['siteInfo']['geoLocation'][
                        'geogLocation']['longitude']
                    network = site['siteInfo']['siteCode'][0]['_network']
                    sitecode = site['siteInfo']['siteCode'][0]['value']

                    hs_json["sitename"] = site_name
                    hs_json["latitude"] = latitude
                    hs_json["longitude"] = longitude
                    hs_json["sitecode"] = sitecode
                    hs_json["network"] = network
                    hs_json["service"] = "SOAP"
                    hs_sites.append(hs_json)
            else:  # If there is just one site within the bounding box, add that site as dictionary object
                hs_json = {}
                site_name = bbox_json['site']['siteInfo']['siteName']
                # site_name = site_name.encode("utf-8")
                latitude = bbox_json['site']['siteInfo'][
                    'geoLocation']['geogLocation']['latitude']
                longitude = bbox_json['site']['siteInfo'][
                    'geoLocation']['geogLocation']['longitude']
                network = bbox_json['site']['siteInfo']['siteCode'][0]['_network']
                sitecode = bbox_json['site']['siteInfo']['siteCode'][0]['value']

                hs_json["sitename"] = site_name
                hs_json["latitude"] = latitude
                hs_json["longitude"] = longitude
                hs_json["sitecode"] = sitecode
                hs_json["network"] = network
                hs_json["service"] = "SOAP"
                hs_sites.append(hs_json)
        except AssertionError as error:
            print("There is an error while parsing the response object ", error)

        return hs_sites

    def recursive_asdict(d):
        """Convert Suds object into serializable format."""
        out = {}
        try:
            for k, v in asdict(d).items():
                if hasattr(v, "__keylist__"):
                    out[k] = recursive_asdict(v)
                elif isinstance(v, list):
                    out[k] = []
                    for item in v:
                        if hasattr(item, "__keylist__"):
                            out[k].append(recursive_asdict(item))
                        else:
                            out[k].append(item)
                else:
                    out[k] = v
        except AssertionError as error:
            print("The following Suds Object cannot be converted to serializable object", error)
        return out

if __name__ == "__main__":
    print("Why are you running the wrapper class file?")

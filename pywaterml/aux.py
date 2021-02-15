import requests
import json
from suds.sudsobject import asdict
from datetime import datetime


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

    def _getValuesHelper(self,k,return_obj):
        #UTC TIME
        try:
            timeUTC = k['@dateTimeUTC']
            time1UTC = timeUTC.replace("T", "-")
            time_splitUTC = time1UTC.split("-")
            year = int(time_splitUTC[0])
            month = int(time_splitUTC[1])
            day = int(time_splitUTC[2])
            hour_minute = time_splitUTC[3].split(":")
            hour = int(hour_minute[0])
            minute = int(hour_minute[1])
            date_stringUTC = datetime(
                year, month, day, hour, minute)
            date_string_convertedUTC = date_stringUTC.strftime("%Y-%m-%d %H:%M:%S")
            return_obj['dateTimeUTC'] = date_string_convertedUTC
        except KeyError as ke:
            return_obj['dateTimeUTC'] = "No Date UTC found"

        #not UTC time
        try:
            time = k['@dateTime']
            time1 = time.replace("T", "-")
            time_split = time1.split("-")
            year = int(time_split[0])
            month = int(time_split[1])
            day = int(time_split[2])
            hour_minute = time_split[3].split(":")
            hour = int(hour_minute[0])
            minute = int(hour_minute[1])
            date_string = datetime(
                year, month, day, hour, minute)
            date_string_converted = date_string.strftime("%Y-%m-%d %H:%M:%S")
            return_obj['dateTime'] = date_string_converted

        except KeyError as ke:
            return_obj['dateTime'] = "No Date found"


        #Value
        try:
            value = float(str(k['#text']))
            return_obj['dataValue'] = value
        except KeyError as ke:
            return_obj['dataValue'] = "No Data provided"

        #@censorCode
        try:
            censorCode = k['@censorCode']
            return_obj['censorCode'] = censorCode
        except KeyError as ke:
            return_obj['censorCode'] = "No Data provided"

        #methodCode
        try:
            methodCode = k['@methodCode']
            return_obj['methodCode'] = methodCode
        except KeyError as ke:
            return_obj['methodCode']= methodCode

        #qualityControlLevel
        try:
            qualityControlLevelCode= k['@qualityControlLevelCode']
            return_obj['qualityControlLevelCode'] = qualityControlLevelCode
        except KeyError as ke:
            return_obj['qualityControlLevelCode'] = "No Data provided"

        #SourceCode
        try:
            sourceCode = k['@sourceCode']
            return_obj['sourceCode'] = sourceCode

        except KeyError as ke:
            return_obj['sourceCode'] = "No Data provided"

        #TimeOffSet
        try:
            timeOffSet = k['@timeOffset']
            return_obj['timeOffSet'] = timeOffSet
        except KeyError as ke:
            return_obj['timeOffset'] = "No Data provided"

        return return_obj

    def _getValuesHelper2(self,times_series,return_object):
        try:
            siteName = times_series['sourceInfo']['siteName'].encode("utf-8")
            return_object['siteName'] = siteName.decode("utf-8")
        except KeyError as ke:
            return_object['siteName'] = "No Data was Provided"

        try:
            return_object['siteCode'] = times_series['sourceInfo']['siteCode']['#text']
        except KeyError as ke:
            return_object['siteCode'] = "No Data was Provided"

        try:
            return_object['network'] = times_series['sourceInfo']['siteCode']['@network']
        except KeyError as ke:
            return_object['network'] = "No Data was Provided"

        try:
            return_object['siteID'] = times_series['sourceInfo']['siteCode']['@siteID']

        except KeyError as ke:
            return_object['siteID'] = "No Data was Provided"

        try:
            return_object['latitude'] = times_series['sourceInfo']['geoLocation']['geogLocation']['latitude']
        except KeyError as ke:
            return_object['latitude'] = "No Data was Provided"

        try:
            return_object['longitude'] = times_series['sourceInfo']['geoLocation']['geogLocation']['longitude']
        except KeyError as ke:
            return_object['longitude'] = "No Data was Provided"

        try:
            return_object['variableName'] = times_series['variable']['variableName']
        except KeyError as ke:
            return_object['variableName'] =  "No Data was Provided"


        try:
            return_object["unitName"] = times_series['variable']['unit']['unitName']
        except KeyError as ke:
            return_object['unitName'] = "No Data was Provided"

        try:
            if times_series['variable']['unit']['unitAbbreviation'] is not None:
                return_object["unitAbbreviation"] = times_series['variable']['unit']['unitAbbreviation']
        except KeyError as ke:
            return_object['unitAbbreviation'] = "No Data was Provided"

        try:
            return_object['dataType'] = times_series['variable']['dataType']
        except KeyError as ke:
            return_object['dataType'] = "No Data was Provided"

        try:
            return_object['noDataValue'] = times_series['variable']['noDataValue']
        except KeyError as ke:
            return_object['noDataValue'] = "No Data was Provided"

        try:
            return_object["isRegular"] = times_series['variable']['timeScale']['@isRegular']
        except KeyError as ke:
            return_object['isRegular'] = "No Data was provided"

        try:
            return_object['timeSupport'] = times_series['variable']['timeScale']['timeSupport']
        except KeyError as ke:
            return_object['timeSupport'] = "No Data was provided"

        try:
            return_object['timeUnitName'] = times_series['variable']['timeScale']['unit']['unitName']
        except KeyError as ke:
            return_object['timeUnitName'] = "No Data was provided"

        try:
            return_object['timeUnitAbbreviation'] = times_series['variable']['timeScale']['unit']['unitAbbreviation']
        except KeyError as ke:
            return_object['timeUnitAbbreviation'] = "No Data was provided"

        try:
            return_object['sampleMedium'] = times_series['variable']['sampleMedium']
        except KeyError as ke:
            return_object['sampleMedium'] = "No Data was Provided"

        try:
            return_object['speciation'] = times_series['variable']['speciation']
        except KeyError as ke:
            return_object['speciation'] = "No Data was Provided"

        return return_object

if __name__ == "__main__":
    print("Why are you running the wrapper class file?")

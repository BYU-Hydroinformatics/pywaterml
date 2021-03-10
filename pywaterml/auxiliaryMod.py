import requests
import json
from suds.sudsobject import asdict
from suds.plugin import *
from suds.plugin import MessagePlugin
from datetime import datetime
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as et
from suds.client import Client

class GetSoapsPlugin(MessagePlugin):
    """
    This class represents the GetSoapsPlugin object for the WaterMLOperations class. The GetSoapsPlugin provides two functions of the MessagePlugin: the reveived and sending functions.
    It helps for debugging purposesrealted to the SOAP protocol.

    Args:
        MessagePlugin: The MessagePlugin currently has (5) hooks:
            - marshalled():: Provides the plugin with the opportunity to inspect/modify the envelope Document before it is sent.
            - sending():: Provides the plugin with the opportunity to inspect/modify the message text before it is sent.
            - received():: Provides the plugin with the opportunity to inspect/modify the received XML text before it is SAX parsed.
            - parsed():: Provides the plugin with the opportunity to inspect/modify the sax parsed DOM tree for the reply before it is unmarshalled.
            - unmarshalled():: Provides the plugin with the opportunity to inspect/modify the unmarshalled reply before it is returned to the caller.

    """
    def __init__(self):
        self.last_sent_raw = None
        self.last_received_raw = None

    def sending(self, context):
        """
        Provides the plugin with the opportunity to inspect/modify the message text before it is sent.
            Args: The Context classes which are passed to the plugin.
        Returns:
            None
        """
        self.last_sent_raw = str(context.envelope)

    def received(self, context):
        """
        Provides the plugin with the opportunity to inspect/modify the received XML text before it is SAX parsed.
            Args: The Context classes which are passed to the plugin.
        Returns:
            None
        """
        self.last_received_raw = str(context.reply)


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
            hs_sites: Dictionary from all the sites of an specific URL with the following data:
                - latitude = The WGS84 latitude in decimal degrees
                - longitude = The WGS84 longitude in decimal degrees
                - site_name = The name of the site
                - network = Network that the site belongs to
                - sitecode = A short unique code of the site
                - siteID = The site ID in the original database
                - fullSiteCode = full site code of the current site. The fullSiteCode of every site is the following string: "network: sitecode"
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
            hs_sites: Dictionary from all the sites of an specific WaterOneFlow web service with the following data:
                - latitude = The WGS84 latitude in decimal degrees
                - longitude = The WGS84 longitude in decimal degrees
                - site_name = The name of the site
                - network = Network that the site belongs to
                - sitecode = A short unique code of the site
                - siteID = The site ID in the original database
                - fullSiteCode = full site code of the current site. The fullSiteCode of every site is the following string: "network: sitecode"

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
                    siteID = site['siteInfo']['siteCode'][0]["_siteID"]
                    hs_json["sitename"] = site_name
                    hs_json["latitude"] = latitude
                    hs_json["longitude"] = longitude
                    hs_json["sitecode"] = sitecode
                    hs_json["network"] = network
                    hs_json["siteID"] = siteID
                    hs_json["fullSiteCode"] = network +":" + sitecode
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
                siteID = bbox_json['site']['siteInfo']['siteCode'][0]["_siteID"]

                hs_json["sitename"] = site_name
                hs_json["latitude"] = latitude
                hs_json["longitude"] = longitude
                hs_json["sitecode"] = sitecode
                hs_json["network"] = network
                hs_json["siteID"] = siteID
                hs_json["fullSiteCode"] = network +":" + sitecode

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
        """
        Helper function to parse and store the content of the dictionary response from the GetValues at the level (['timeSeriesResponse']['timeSeries']['values']['value'])
        into a new dictionary. The data stored into this dictionary from the GetValues response is the following:

            - dateTimeUTC: The UTC time of the observation.
            - dateTime: The local date/time of the observation.
            - dataValue: Data value from the observation.
            - censorCode: The code for censored observations.  Possible values are nc (not censored), gt(greater than), lt (less than), nd (non-detect), pnq (present but not quantified)
            - methodCode: The code of the method or instrument used for the observation
            - qualityControlLevelCode: The code of the quality control level.  Possible values are -9999(Unknown), 0 (Raw data), 1 (Quality controlled data), 2 (Derived products), 3 (Interpretedproducts), 4 (Knowledge products)
            - sourceCode: The code of the data source
            - timeOffSet: The difference between local time and UTC time in hours.

        This function is only stores half of the reponse from the GetValues method, and it is usually used with the _getValuesHelper2 function that stores the other half of the function.
        Args:
            k: GetValues response dictionary at level -> (['timeSeriesResponse']['timeSeries']['values']['value'])
            return_obj: python dictionary that will store the data from teh GetValues response.
        Returns:
            return_obj: python dictionary containing data from the GetValues response.
        """
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
            return_obj['dataValue'] = "No Data Provided"

        #@censorCode
        try:
            censorCode = k['@censorCode']
            return_obj['censorCode'] = censorCode
        except KeyError as ke:
            return_obj['censorCode'] = "No Data Provided"

        #methodCode
        try:
            methodCode = k['@methodCode']
            return_obj['methodCode'] = methodCode
        except KeyError as ke:
            return_obj['methodCode']= "No Data Provided"

        #qualityControlLevel
        try:
            qualityControlLevelCode= k['@qualityControlLevelCode']
            return_obj['qualityControlLevelCode'] = qualityControlLevelCode
        except KeyError as ke:
            return_obj['qualityControlLevelCode'] = "No Data Provided"

        #SourceCode
        try:
            sourceCode = k['@sourceCode']
            return_obj['sourceCode'] = sourceCode

        except KeyError as ke:
            return_obj['sourceCode'] = "No Data Provided"

        #TimeOffSet
        try:
            timeOffSet = k['@timeOffset']
            return_obj['timeOffSet'] = timeOffSet
        except KeyError as ke:
            return_obj['timeOffset'] = "No Data Provided"

        return return_obj

    def _getValuesHelper2(self,times_series,return_object):
        """
        Helper function to parse and store the content of the dictionary response from the GetValues at the level (['timeSeriesResponse']['timeSeries']['values']['value']) into a new dictionary. The data stored into this dictionary from the GetValues response is the following:
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

        This function is only stores half of the reponse from the GetValues method, and it is usually used with the _getValuesHelper function that stores the other half of the function.
        Args:
            times_series: GetValues response dictionary at level -> (['timeSeriesResponse']['timeSeries']['values']['value'])
            return_object: python dictionary that will store the data from teh GetValues response.
        Returns:
            return_object: python dictionary containing data from the GetValues response.
        """
        try:
            try:

                siteName = times_series['sourceInfo']['siteName'].encode("utf-8")
                # siteName = times_series['sourceInfo']['siteName']
                # return_object['siteName'] = siteName
                return_object['siteName'] = siteName.decode("utf-8")
            except KeyError as ke:
                # print(ke)
                return_object['siteName'] = "No Data was Provided"

            try:
                # print(times_series)
                return_object['siteCode'] = times_series['sourceInfo']['siteCode']['#text']
                # print(return_object)
            except KeyError as ke:
                # print(ke)
                # print(return_object)
                return_object['siteCode'] = "No Data was Provided"

            try:
                return_object['network'] = times_series['sourceInfo']['siteCode']['@network']
            except KeyError as ke:
                # print(ke)
                # print(return_object)

                return_object['network'] = "No Data was Provided"

            try:
                return_object['siteID'] = times_series['sourceInfo']['siteCode']['@siteID']
            except KeyError as ke:
                # print(ke)
                # print(return_object)

                return_object['siteID'] = "No Data was Provided"

            try:
                return_object['latitude'] = times_series['sourceInfo']['geoLocation']['geogLocation']['latitude']
            except KeyError as ke:
                # print(ke)
                # print(return_object)

                return_object['latitude'] = "No Data was Provided"

            try:
                return_object['longitude'] = times_series['sourceInfo']['geoLocation']['geogLocation']['longitude']
            except KeyError as ke:
                # print(ke)
                # print(return_object)

                return_object['longitude'] = "No Data was Provided"

            try:
                return_object['variableName'] = times_series['variable']['variableName']
            except KeyError as ke:
                # print(ke)
                # print(return_object)

                return_object['variableName'] =  "No Data was Provided"


            try:
                return_object["unitName"] = times_series['variable']['unit']['unitName']
            except KeyError as ke:
                # print(ke)
                # print(return_object)

                return_object['unitName'] = "No Data was Provided"

            try:
                if times_series['variable']['unit']['unitAbbreviation'] is not None:
                    return_object["unitAbbreviation"] = times_series['variable']['unit']['unitAbbreviation']
            except KeyError as ke:
                # print(ke)
                # print(return_object)

                return_object['unitAbbreviation'] = "No Data was Provided"

            try:
                return_object['dataType'] = times_series['variable']['dataType']
            except KeyError as ke:
                # print(ke)
                # print(return_object)

                return_object['dataType'] = "No Data was Provided"

            try:
                return_object['noDataValue'] = times_series['variable']['noDataValue']
            except KeyError as ke:
                # print(ke)
                # print(return_object)

                return_object['noDataValue'] = "No Data was Provided"

            try:
                return_object["isRegular"] = times_series['variable']['timeScale']['@isRegular']
            except KeyError as ke:
                # print(ke)
                # print(return_object)

                return_object['isRegular'] = "No Data was provided"

            try:
                return_object['timeSupport'] = times_series['variable']['timeScale']['timeSupport']
            except KeyError as ke:
                # print(ke)
                # print(return_object)

                return_object['timeSupport'] = "No Data was provided"

            try:
                return_object['timeUnitName'] = times_series['variable']['timeScale']['unit']['unitName']
            except KeyError as ke:
                # print(ke)
                # print(return_object)

                return_object['timeUnitName'] = "No Data was provided"

            try:
                return_object['timeUnitAbbreviation'] = times_series['variable']['timeScale']['unit']['unitAbbreviation']
            except KeyError as ke:
                # print(ke)
                # print(return_object)

                return_object['timeUnitAbbreviation'] = "No Data was provided"

            try:
                return_object['sampleMedium'] = times_series['variable']['sampleMedium']
            except KeyError as ke:
                # print(ke)
                # print(return_object)

                return_object['sampleMedium'] = "No Data was Provided"

            try:
                return_object['speciation'] = times_series['variable']['speciation']
            except KeyError as ke:
                # print(ke)
                # print(return_object)

                return_object['speciation'] = "No Data was Provided"
        except Exception as e:
            return_object = return_object
            # print(e)
            # print(return_object)

            # return
        return return_object

    def _getSiteInfoHelper(self,object_siteInfo,object_methods):
        """
        Helper function to parse and store the content of two dictionaries:

            - object_methods = GetSiteInfoResponse ['sitesResponse']['site']['seriesCatalog']['series']
            - object_siteInfo = GetSiteInfoResponse ['sitesResponse']['site']['siteInfo']

        Both dictionaries containing the response from the GetSiteInfo at store the following content into a new dictionary:

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

        Args:
            object_siteInfo: Contains metadata associated to the site.
            object_methods: Contains a list of <series>, which are unique combinations of site, variable and time intervals that specify a sequence of observations.
        Returns:
            return_obj: python dictionary containing data from the GetSiteInfo response.
        """
        return_obj = {}
        try:
            # return_obj['siteName'] = object_siteInfo['siteName']
            siteName = object_siteInfo['siteName'].encode("utf-8")
            # return_object['siteName'] = siteName
            return_obj['siteName'] = siteName.decode("utf-8")
        except KeyError as ke:
            return_obj['siteName'] = "No Data was Provided"

        try:
            return_obj['latitude'] = object_siteInfo['geoLocation']['geogLocation']['latitude']
        except KeyError as ke:
            return_obj['latitude'] = "No Data was Provided"

        try:
            return_obj['longitude'] = object_siteInfo['geoLocation']['geogLocation']['longitude']
        except KeyError as ke:
            return_obj['longitude'] = "No Data was Provided"

        try:
            return_obj['network'] = object_siteInfo['siteCode']['@network']
        except KeyError as ke:
            return_obj['network'] = "No Data was Provided"

        try:
            return_obj['siteCode'] = object_siteInfo['siteCode']['#text']
        except KeyError as ke:
            return_obj['siteCode'] = "No Data was Provided"

        try:
            return_obj['fullSiteCode'] = return_obj['network'] + ":" + return_obj['siteCode']
        except KeyError as ke:
            return_obj['fullSiteCode'] = "No Data was Provided"

        try:
            return_obj['variableName'] = object_methods['variable']['variableName']
        except KeyError as ke:
            return_obj['variableName'] = "No Data was Provided"

        try:
            return_obj['variableCode'] = object_methods['variable']['variableCode']['#text']
        except KeyError as ke:
            return_obj['variableCode'] = "No Data was Provided"

        try:
            return_obj['fullVariableCode'] = return_obj['network'] + ":" + return_obj['variableCode']
        except KeyError as ke:
            return_obj['fullVariableCode'] = "No Data was Provided"

        try:
            return_obj['variableCount'] = object_methods['valueCount']
        except KeyError as ke:
            return_obj['variableCount'] = "No Data was Provided"

        try:
            return_obj['dataType'] = object_methods['variable']['dataType']
        except KeyError as ke:
            return_obj['dataType'] = "No Data was Provided"

        try:
            return_obj['valueType'] = object_methods['variable']['valueType']
        except KeyError as ke:
            return_obj['valueType'] = "No Data was Provided"

        try:
            return_obj['generalCategory'] = object_methods['variable']['generalCategory']
        except KeyError as ke:
            return_obj['generalCategory'] = "No Data was Provided"

        try:
            return_obj['noDataValue'] = object_methods['variable']['noDataValue']
        except KeyError as ke:
            return_obj['noDataValue'] = "No Data was Provided"

        try:
            return_obj['sampleMedium'] = object_methods['variable']['sampleMedium']
        except KeyError as ke:
            return_obj['sampleMedium'] = "No Data was Provided"

        try:
            return_obj['speciation'] = object_methods['variable']['speciation']
        except KeyError as ke:
            return_obj['speciation'] = "No Data was Provided"
        try:
            return_obj['timeUnitAbbreviation'] = object_methods['variable']['timeScale']['unit']['unitAbbreviation']
        except KeyError as ke:
            return_obj['timeUnitAbbreviation'] = "No Data was Provided"

        try:
            return_obj['timeUnitName'] = object_methods['variable']['timeScale']['unit']['unitName']
        except KeyError as ke:
            return_obj['timeUnitName'] = "No Data was Provided"

        try:
            return_obj['timeUnitType'] = object_methods['variable']['timeScale']['unit']['unitType']
        except KeyError as ke:
            return_obj['timeUnitType'] = "No Data was Provided"

        try:
            return_obj['timeSupport'] = object_methods['variable']['timeScale']['timeSupport']
        except KeyError as ke:
            return_obj['timeSupport'] = "No Data was Provided"

        try:
            return_obj['isRegular'] = object_methods['variable']['timeScale']['@isRegular']
        except KeyError as ke:
            return_obj['isRegular'] = "No Data was Provided"

        try:
            return_obj['unitAbbreviation'] = object_methods['variable']['unit']['unitAbbreviation']
        except KeyError as ke:
            return_obj['unitAbbreviation'] = "No Data was Provided"

        try:
            return_obj['unitName'] = object_methods['variable']['unit']['unitName']
        except KeyError as ke:
            return_obj['unitName'] = "No Data was Provided"

        try:
            return_obj['unitType'] = object_methods['variable']['unit']['unitType']
        except KeyError as ke:
            return_obj['unitType'] = "No Data was Provided"

        if 'method' in object_methods:
            return_obj['methodID'] = object_methods['method']['@methodID']
            return_obj['methodDescription'] = object_methods['method']['methodDescription']
        else:
            return_obj['methodID'] = "No Method Id was provided"
            return_obj['methodDescription'] = "No Method Description was provided"


        try:
            return_obj['qualityControlLevelID'] = object_methods['qualityControlLevel']['@qualityControlLevelID']
        except KeyError as ke:
            return_obj['qualityControlLevelID'] = "No Data was Provided"

        try:
            return_obj['definition'] = object_methods['qualityControlLevel']['definition']
        except KeyError as ke:
            return_obj['definition'] = "No Data was Provided"

        try:
            return_obj['qualityControlLevelCode'] = object_methods['qualityControlLevel']['qualityControlLevelCode']
        except KeyError as ke:
            return_obj['qualityControlLevelCode'] = "No Data was Provided"

        try:
            return_obj['citation'] = object_methods['source']['citation']
        except KeyError as ke:
            return_obj['citation'] = "No Data was Provided"

        try:
            return_obj['organization'] = object_methods['source']['organization']
        except KeyError as ke:
            return_obj['organization'] = "No Data was Provided"

        try:
            return_obj['description'] = object_methods['source']['sourceDescription']
        except KeyError as ke:
            return_obj['description'] = "No Data was Provided"

        try:
            return_obj['beginDateTime'] = object_methods['variableTimeInterval']['beginDateTime']
        except KeyError as ke:
            return_obj['beginDateTime'] = "No Data was Provided"

        try:
            return_obj['endDateTime'] = object_methods['variableTimeInterval']['endDateTime']
        except KeyError as ke:
            return_obj['endDateTime'] = "No Data was Provided"

        try:
            return_obj['beginDateTimeUTC'] = object_methods['variableTimeInterval']['beginDateTimeUTC']
        except KeyError as ke:
            return_obj['beginDateTimeUTC'] = "No Data was Provided"

        try:
            return_obj['endDateTimeUTC'] = object_methods['variableTimeInterval']['endDateTimeUTC']
        except KeyError as ke:
            return_obj['endDateTimeUTC'] = "No Data was Provided"

        return return_obj

    def _getVariablesHelper(self,one_variable, return_object):
        """
        Helper function to parse and store the content of the GetValues response dictionary at the level:

            - one_variable = GetVariablesResponse ['variablesResponse']['variables']['variable']

        The dictionary containing the response from the GetValues method stores the following content into a new dictionary:

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

        Args:
            one_variable: Contains metadata associated to the different variables of the site.
            return_object: python dictionary that will store the data from the GetVariables response.

        Returns:
            return_object: python dictionary containing data from the GetVariables response.
        """
        try:
            return_object['variableName'] = one_variable['variableName']
        except KeyError as ke:
            return_object['variableName'] = "No Data Provided"

        try:
            return_object['variableCode'] = one_variable['variableCode']['#text']
        except KeyError as ke:
            return_object['variableName'] = "No Data Provided"

        try:
            return_object['valueType']= one_variable['valueType']
        except KeyError as ke:
            return_object['valueType'] = "No Data Provided"

        try:
            return_object['dataType']= one_variable['dataType']
        except KeyError as ke:
            return_object['dataType'] = "No Data Provided"
        try:
            return_object['generalCategory'] = one_variable['generalCategory']
        except KeyError as ke:
            return_object['generalCategory'] = "No Data Provided"
        try:
            return_object['sampleMedium'] = one_variable['sampleMedium']
        except KeyError as ke:
            return_object['sampleMedium'] = "No Data Provided"
        try:
            return_object['unitName'] = one_variable['unit']['unitName']
        except KeyError as ke:
            return_object['unitName'] = "No Data Provided"
        try:
            return_object['unitType'] = one_variable['unit']['unitType']
        except KeyError as ke:
            return_object['unitType'] = "No Data Provided"
        try:
            return_object['unitAbbreviation'] = one_variable['unit']['unitAbbreviation']
        except KeyError as ke:
            return_object['unitAbbreviation'] = "No Data Provided"
        try:
            return_object['noDataValue'] = one_variable['noDataValue']
        except KeyError as ke:
            return_object['noDataValue'] = "No Data Provided"
        try:
            return_object['isRegular'] = one_variable['variableCode']['@default']
        except KeyError as ke:
            return_object['isRegular'] = "No Data Provided"
        try:
            return_object['timeUnitName'] = one_variable['timeScale']['unit']['unitName']
        except KeyError as ke:
            return_object['timeUnitName'] = "No Data Provided"
        try:
            return_object['timeUnitAbbreviation'] = one_variable['timeScale']['unit']['unitAbbreviation']
        except KeyError as ke:
            return_object['timeUnitAbbreviation'] = "No Data Provided"
        try:
            return_object['timeSupport'] = one_variable['timeScale']['timeSupport']
        except KeyError as ke:
            return_object['timeSupport'] = "No Data Provided"
        try:
            return_object['speciation'] = one_variable['speciation']
        except KeyError as ke:
            return_object['speciation'] = "No Data Provided"

        return return_object

    # def return_option(self,return_object):

    def _parseService(self,centralUrl):
        """
        Helper function to parse JSON data into a python dictionary. It is used in the WaterMLOperations GetWaterOneFlowServiceInfo() function. If the WaterOneFlow web service endpoint is
        not accesible though the suds library.
        Args:
            centralUrl: URL from a WaterOneFlow web servicee to access a HIS catalog
        Returns:
            services: Dictionary from all the web services contained in the WaterOneFlow web service endpoint. The folllowing data is returned for each service:
                - servURL: URL of the WaterOneFlow  web service
                - Title: title of the WaterOneFlow  web service
                - organization: supervising organization of the WaterOneFlow  web service
                - aabstract: abstract of the WaterOneFlow  web service
        """
        url_trim = centralUrl.split("?WSDL")[0]
        url = url_trim + "/GetWaterOneFlowServiceInfo"
        # print(url)
        response = urllib.request.urlopen(url)
        data = response.read()
        parse_xml = et.fromstring(data)

        services = []
        for item in parse_xml:
            newService = {}

            for child in item:
                if child.tag == '{http://hiscentral.cuahsi.org/20100205/}servURL':
                    newService['servURL'] = child.text
                if child.tag == '{http://hiscentral.cuahsi.org/20100205/}Title':
                    newService['Title'] = child.text
                if child.tag == '{http://hiscentral.cuahsi.org/20100205/}organization':
                    newService['organization'] = child.text
                if child.tag == '{http://hiscentral.cuahsi.org/20100205/}aabstract':
                    newService['aabstract'] = child.text

            services.append(newService)

        return services

    def _giveServices(self,services,filter_serv=None):
        # print("hola")
        json_response = {}
        hs_list = []
        hs_list_notworking=[]
        for i in services:
            # print(i)
            hs = {}
            url = i['servURL']
            if not url.endswith('?WSDL'):
                url = url + "?WSDL"
            title = i['Title']
            description = "None was provided by the organiation in charge of the Web Service"
            if 'aabstract' in i:
                description = i['aabstract']
            if filter_serv is not None:
                if title in filter_serv:
                    hs['url'] = url
                    hs['title'] = title
                    hs['description'] = description
                    try:
                        url_client = Client(url)
                        hs_list.append(hs)
                    except Exception as e:
                        hs_list_notworking.append(hs)

            else:
                hs['url'] = url
                hs['title'] = title
                hs['description'] = description
                try:
                    url_client = Client(url)
                    hs_list.append(hs)
                except Exception as e:
                    hs_list_notworking.append(hs)

                    # error_list.append(hs)
                # hs_list['servers'] = hs_list
                # list['errors'] = error_list
        json_response['working'] = hs_list
        json_response['failed'] = hs_list_notworking
        return json_response

if __name__ == "__main__":
    print("Why are you running the wrapper class file?")

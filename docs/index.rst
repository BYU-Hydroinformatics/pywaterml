.. pyWaterML documentation master file, created by
   sphinx-quickstart on Tue Dec  1 18:57:18 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyWaterML Documentation
=====================================
pyWaterMLis a python package developed by the Hydroinformatics laboratory in the Civil Engineering at Brigham Young University. pyWaterML allows the user to work with endpoints that are compliant with WaterML: Fetch and Analyze Data from 'WaterML' and 'WaterOneFlow' Web Services
Lets you connect to any of the 'Consortium of Universities for the Advancement of Hydrological Science, Inc.' ('CUAHSI') Water Data Center 'WaterOneFlow' web services and read any 'WaterML' time series data file. To see list of available web services, see http://hiscentral.cuahsi.org. All versions of 'WaterML' (1.0, 1.1 and 2.0) and both types of the web service protocol ('SOAP' and 'REST') are supported.
The package has multiple files which are: waterML, analyzeData, aux. The main module is the waterML while analyzeData and aux are modules that helps the main waterML package. The main waterML module has main data download functions of the 'WaterOneFlow' web services:

1) GetSites(): Get all the sites from a endpoint that complies to the SOAP protocol. The GetSites() function is similar to the GetSites() WaterML function.
2) GetSitesByBoxObject(): Get all the sites from a bounding box from a endpoint that complies to the SOAP protocol. The GetSitesByBoxObject() function is similar to the GetSitesByBoxObject() WaterML function.
3) GetVariables(): Get all the variables from a endpoint that complies to the SOAP protocol. GetVariables() function is similar to the GetVariables() WaterML function
4) GetSiteInfo(): Get the information of a given site. GetSiteInfo() function is similar to the GetSiteInfo() WaterML function.
5) GetValues(): Get the specific values for an specific variable in a site. GetValues() function is similar to the GetValues() WaterML function.
6) AvailableServices(): Get the WaterOneFlow web services that are available from a WaterOneFlow service containing a HIS catalog.
7) GetWaterOneFlowServiceInfo(): Get all registered data services from a given WaterOneFlow Web service containing a HIS catalog. GetWaterOneFlowServiceInfo can be regarded as a special case of GetServicesInBox2, as the former requests the returns for the global area.

The waterML module also has functions that add functionality to the 'WaterOneFlow' web services. The extra functionality includes the following functions:

1) GetSitesByVariable(): Get the specific sites according to a variable search array from a endpoint that complies to the SOAP protocol. The GetSitesByVariable() is an addition to the WaterML functions because it allows the user to retrieve sites that contains the epecific site/s.
2) GetInterpolation(): Interpolates the data given by the GetValues function in order to fix datasets with missing values. Three ooptions for interpolation are offered: mean, backward, forward. The default is the mean interpolation.
3) GetMonthlyAverage(): Gets the monthly averages for a given variable, or from the response given by the GetValues function for a given site.
4) GetClustersMonthlyAvg(): Gets "n" number of clusters using dtw time series interpolation for a given variable.

pyWaterML strives to be an intuitive python package for accesing WaterML information, and it also brings new functionality to the retrieved data from 'WaterOneFlow' web services.
pyWaterML also brings some basic machine learning clsutering based on monthly average for different variables.
The following links will result useful to the users that want to contribute or experiment the package:

1) `Source Code <https://github.com/romer8/pywaterml>`__
2) `Google Collaboratory Example <https://colab.research.google.com/drive/1R9T-cu1l7KgXcNU7wLGfcUhKOOY0Ltvg#scrollTo=axKiaVU1pjQe>`__

.. toctree::
   :maxdepth: 1
   :name: mastertoc
   :caption: Contents:

   WaterML Module Methods Information <waterML>
   Auxiliary Module Methods Information <auxiliaryMod>
   WaterAnalityca Module Methods Information <analitica>
   About the BYU Hydroinformatics group <hydroinformatics>

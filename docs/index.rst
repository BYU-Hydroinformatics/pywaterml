.. pyWaterML documentation master file, created by
   sphinx-quickstart on Tue Dec  1 18:57:18 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyWaterML's documentation
=====================================

pyWaterMLis a python package to work with endpoints that are compliant with WaterML: Fetch and Analyze Data from 'WaterML' and 'WaterOneFlow' Web Services
Lets you connect to any of the 'Consortium of Universities for the Advancement of Hydrological Science, Inc.' ('CUAHSI') Water Data Center 'WaterOneFlow' web services and read any 'WaterML' time series data file. To see list of available web services, see <http://hiscentral.cuahsi.org>. All versions of 'WaterML' (1.0, 1.1 and 2.0) and both types of the web service protocol ('SOAP' and 'REST') are supported.
The package has multiple files which are: waterML, analyzeData, aux. The main module is the waterML while analyzeData and aux are modules that helps the main waterML package. The main waterML module has main data download functions of the 'WaterOneFlow' web services:

1) GetSites():
2) GetSitesByBoxObject()
3) GetVariables()
4) GetSiteInfo()
5) GetValues()

The waterML module also has functions that add functionality to the 'WaterOneFlow' web services. The extra functionality includes the following functions:

1) GetSitesByVariable()
2) Interpolate()
3) GetMonthlyAverage()
4) GetClustersMonthlyAvg()

.. toctree::
   :maxdepth: 1
   :name: mastertoc
   :caption: Contents:

   waterML

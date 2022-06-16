from pywaterml.waterML import WaterMLOperations
import pytest


Your_Personal_Token_Identifier = 'whos-61c7173d-b0cf-444e-b6f0-ae9cfc221635'


params_services = [
    "https://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL",
    f'https://whos.geodab.eu/gs-service/services/essi/token/{Your_Personal_Token_Identifier}/view/gs-view-and(whos,gs-view-source(onametStations))/cuahsi_1_1.asmx?WSDL',
    f'https://whos.geodab.eu/gs-service/services/essi/token/{Your_Personal_Token_Identifier}/view/gs-view-and(whos,gs-view-source(argentina-ina))/cuahsi_1_1.asmx?WSDL'
]



@pytest.fixture(params=params_services)
def water(request,scope="class"):
    water = WaterMLOperations(url = request.param)
    return water

@pytest.fixture    
def sites(water,scope="class"):
    sites = water.GetSites()
    return sites

@pytest.fixture(params=[0,1])    
def fullSiteCode(request,sites,scope="class"):
    return sites[request.param]['fullSiteCode']

@pytest.fixture(params=[0,1])    
def variableCodeMetaData(request,siteInfo,scope="class"):
    code = siteInfo['siteInfo'][request.param]['fullVariableCode']
    start_date = siteInfo['siteInfo'][request.param]['beginDateTime'].split('T')[0]
    end_date = siteInfo['siteInfo'][request.param]['endDateTime'].split('T')[0]
    return [code,start_date, end_date] 

@pytest.fixture    
def siteInfo(water,fullSiteCode,scope="class"):
    siteInfo =  water.GetSiteInfo(fullSiteCode)
    return siteInfo

@pytest.fixture    
def variableValues(request,water,fullSiteCode,variableCodeMetaData,scope="class"):
    fullVariableCodeFirstVariable = variableCodeMetaData[0]
    start_date = variableCodeMetaData[1]
    end_date = variableCodeMetaData[2]
    variableResponse = water.GetValues(fullSiteCode, fullVariableCodeFirstVariable, start_date, end_date)
    return variableResponse


class TestWaterMLViewsCommonFunctions: 
    def test_GetSites(self,sites):
        assert sites, f'Retrieved {len(sites)} Sites'

    def test_GetVariables(self,water):
        variables = water.GetVariables()
        assert len(variables['variables']) > 0, f'Retrieved {len(variables["variables"])} variables'
        
    def test_GetSiteInfo(self,siteInfo):
        assert len(siteInfo['siteInfo']) > 0, f'Retrieved {len(siteInfo["siteInfo"])} variables'
    
    def test_GetValues(self,variableValues):
        assert 'values' in variableValues, f'Retrieved {len(variableValues["values"])} data points'



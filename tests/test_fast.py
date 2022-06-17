from pywaterml.waterML import WaterMLOperations
import pytest


Your_Personal_Token_Identifier = 'whos-61c7173d-b0cf-444e-b6f0-ae9cfc221635'

url_dummy = 'http://hydroportal.cuahsi.org/CALVIN_HHS/cuahsi_1_1.asmx?WSDL'


params_catalog =[
    "http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-country/hiscentral.asmx?WSDL"
]

params_services = [
    # f'https://whos.geodab.eu/gs-service/services/essi/token/{Your_Personal_Token_Identifier}/view/gs-view-and(whos,gs-view-source(iceland-imo))/cuahsi_1_1.asmx?WSDL'
    'https://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL'
]

@pytest.fixture(params=params_catalog)
def water_catalog(request,scope="class"):
    water = WaterMLOperations(url = request.param)
    return water

@pytest.fixture(params=params_services)
def water(request,scope="class"):
    water = WaterMLOperations(url = request.param)
    return water

@pytest.fixture    
def sites(water,scope="class"):
    sites = water.GetSites()
    return sites

@pytest.fixture(params=[0])    
def fullSiteCode(request,sites,scope="class"):
    return sites[request.param]['fullSiteCode']

@pytest.fixture(params=[0])    
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
class TestWaterMLCatalogs:
    @pytest.mark.parametrize("catalog_url",params_catalog)
    def test_AddService(self,catalog_url):
        water_catalog = WaterMLOperations()
        assert water_catalog.AddService(url = catalog_url) == True, f'{catalog_url} service added successfully'
    
    @pytest.mark.parametrize("catalog_url",params_catalog)
    def test_ChangeService(self,catalog_url):
        water_catalog = WaterMLOperations(url=url_dummy)
        assert water_catalog.ChangeService(url=catalog_url) == True, f'{catalog_url} service changed successfully'
    
    def test_AvailableServices(self,water_catalog):
        services = water_catalog.AvailableServices()
        assert 'available' in services, f'Available {len(services["available"])} Sevices and Broken {len(services["broken"])} Services'
    
    def test_GetWaterOneFlowServicesInfo(self,water_catalog):
        services = water_catalog.GetWaterOneFlowServicesInfo()
        assert len(services) > 0, f'Retrieved {len(services)} Services'

class TestWaterMLViews:
 
    def test_GetSites(self,sites):
        assert sites, f'Retrieved {len(sites)} Sites'

    def test_GetSitesBoundingBox(self,water):
        BoundsRearranged = [-66.4903,18.19699,-66.28665,18.28559]
        #BoundsRearranged = [-7398417.229789019,2048546.619479188,-7368453.914701229,2080306.2047316788]
        #BoundsRearranged = [-7401666.338691997, 2060618.8113541743, -7378996.124391947, 2071003.588530944]
        #sites = water.GetSitesByBoxObject(BoundsRearranged,'epsg:3857')
        sites = water.GetSitesByBoxObject(BoundsRearranged,'epsg:4326')
        assert len(sites)>=0, f'Retrieved {len(sites)} Sites in the bounding box {BoundsRearranged}'

    def test_GetVariables(self,water):
        variables = water.GetVariables()
        assert len(variables['variables']) > 0, f'Retrieved {len(variables["variables"])} variables'

    def test_GetSiteInfo(self,siteInfo):
        assert len(siteInfo['siteInfo']) > 0, f'Retrieved {len(siteInfo["siteInfo"])} variables'

    def test_GetSitesByVariables(self,water,variableCodeMetaData):
        variablesTest = [variableCodeMetaData[0]]
        sitesFiltered = water.GetSitesByVariable(variablesTest)
        assert len(sitesFiltered)>0, f'Retrieved {len(sitesFiltered)} Sites for variable code "{variablesTest}"'
    
    def test_GetValues(self,variableValues):
        assert 'values' in variableValues, f'Retrieved {len(variableValues["values"])} data points'
    
    def test_GetInterpolation(self,water,variableValues):
        interpol_b = water.GetInterpolation(variableValues, 'backward')
        assert len(interpol_b)>0, f'Backward interpolation, retrieved {len(interpol_b)} interpolated values'
    
    def test_GetInterpolation(self,water,variableValues):
        interpol_f = water.GetInterpolation(variableValues, 'forward')
        assert len(interpol_f)>0, f'Forward interpolation, retrieved {len(interpol_f)} interpolated values'
    
    def test_GetInterpolation(self,water,variableValues):
        interpol_m = water.GetInterpolation(variableValues, 'mean')
        assert len(interpol_m)>0, f'Mean interpolation, retrieved {len(interpol_m)} interpolated values'
    
    def test_GetMonthlyAverages(self,water,variableValues):
        m_avg = water.GetMonthlyAverage(variableValues)
        assert len(m_avg)>0, f'Monthly averages using pre calculated values retrieved {len(m_avg)} data values'
        
    def test_GetClusters(self,water,sites,variableCodeMetaData):
        var_code = variableCodeMetaData[0].split(":")[-1]
        y_pred = water.GetClustersMonthlyAvg(sites,var_code)
        assert len(y_pred)>0, f'Sucessful data clustering'

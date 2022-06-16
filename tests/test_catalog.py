from pywaterml.waterML import WaterMLOperations
import pytest


Your_Personal_Token_Identifier = 'whos-61c7173d-b0cf-444e-b6f0-ae9cfc221635'

url_dummy = 'http://hydroportal.cuahsi.org/CALVIN_HHS/cuahsi_1_1.asmx?WSDL'


params_catalog =[
    "http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-country/hiscentral.asmx?WSDL",
    "http://gs-service-production.geodab.eu/gs-service/services/essi/view/whos-transboundary/hiscentral.asmx?WSDL",
    "https://hiscentral.cuahsi.org/webservices/hiscentral.asmx?WSDL"
    
]


@pytest.fixture(params=params_catalog)
def water_catalog(request,scope="class"):
    water = WaterMLOperations(url = request.param)
    return water


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



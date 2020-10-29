from waterML import WaterMLOperations


url_testing = "http://hydroportal.cuahsi.org/para_la_naturaleza/cuahsi_1_1.asmx?WSDL"
water = WaterMLOperations(url = url_testing)

def main():
    sites = water.GetSites()
    variables = water.GetVariables()
    print("************SITES***************")
    print(sites)
    print("************VARIABLES***********")
    print(variables)
    print("******************CHANGE URL***********")
    water.ChangeEndpoint("http://128.187.106.131/app/index.php/dr/services/cuahsi_1_1.asmx?WSDL")
    sites = water.GetSites()
    variables = water.GetVariables()
    print("************SITES***************")
    print(sites)
    print("************VARIABLES***********")
    print(variables)
if __name__ == "__main__":
    main()

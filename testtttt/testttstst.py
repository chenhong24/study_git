from suds import client

#
# cli = client.Client(url="http://ws.lemonban.com/sms-service-war-1.0/ws/smsFacade.ws?wsdl")
# print(cli)
#
# data = {"client_ip": "125.1.2.3", "teml_id": "1", "mobile": "13345673456"}
# try:
#     res = cli.service.sendMCode(data)
# except Exception as e:
#     print(e.fault)
# else:
#     print(dict(res))


cli = client.Client(url="http://www.webxml.com.cn/WebServices/IpAddressSearchWebService.asmx?wsdl")
print(cli)

theIpAddress = "125.1.2.44"
res = cli.service.getCountryCityByIp(theIpAddress)
print(dict(res))

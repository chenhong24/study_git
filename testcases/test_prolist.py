import unittest
import jsonpath
import os
from library.ddt import ddt, data
from common.readexcel import ReadExcel
from common.handler_path import DATADIR
from common.handleconfig import conf
from common.handler_requests import SendRequest
from common.handlelog import log
from common.connectdb import DB
from common.handler_data import CaseData

case_file = os.path.join(DATADIR, "apicases.xlsx")


@ddt
class TestList(unittest.TestCase):
    excel = ReadExcel(case_file, "list")
    cases = excel.read_data()
    request = SendRequest()
    db = DB()

    @classmethod
    def setUpClass(cls) -> None:
        """进行登录"""
        # 1、准备登录的数据
        url = conf.get("env", "url") + "/member/login"
        data = {
            "mobile_phone": conf.get("test_data", "admin_phone"),
            "pwd": conf.get("test_data", "admin_pwd")
        }
        headers = eval(conf.get("env", "headers"))
        # 3、发送请求，进行登录
        response = cls.request.send(url=url, method="post", json=data, headers=headers)
        # 获取返回的数据
        res = response.json()
        # 3、提取token,保存为类属性
        token = jsonpath.jsonpath(res, "$..token")[0]
        token_type = jsonpath.jsonpath(res, "$..token_type")[0]
        # 将提取到的token设为CaseData类属性
        CaseData.admin_token_value = token_type + " " + token

    @data(*cases)
    def test_list(self, case):
        # 第一步，准备用例数据
        url = conf.get("env", "url") + case["url"]
        method = case["method"]
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(CaseData, "admin_token_value")
        expected = eval(case["expected"])
        row = case["case_id"] + 1

        # 第二步，发送请求，获取结果
        response = self.request.send(url=url, method=method, json=data, headers=headers)
        res = response.json()

        # 第三步，断言比对预期结果和实际结果
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])

        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="未通过")
            print("预期结果", expected)
            print("实际结果", res)
            log.error("用例{}执行未通过".format(case["title"]))
            log.exception(e)
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
            print("预期结果", expected)
            print("实际结果", res)
            log.error("用例{}执行通过".format(case["title"]))

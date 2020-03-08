import unittest
import os
import jsonpath
from library.ddt import ddt, data
from common.readexcel import ReadExcel
from common.handler_path import DATADIR
from common.handleconfig import conf
from common.handler_requests import SendRequest
from common.handlelog import log
from common.handler_data import CaseData, replace_data

case_file = os.path.join(DATADIR, "apicases.xlsx")

"""
需要有标：管理员登录，加标，审核
用户登录
投资用例的执行
"""


@ddt
class TestInvest(unittest.TestCase):
    excel = ReadExcel(case_file, "invest")
    cases = excel.read_data()
    request = SendRequest()

    @data(*cases)
    def test_invest(self, case):
        # 第一步，准备用例数据
        url = conf.get("env", "url") + case["url"]
        method = case["method"]
        case["data"] = replace_data(case["data"])
        data = eval(case["data"])
        headers = eval(conf.get("env", "headers"))
        if case["interface"] != "login":
            headers["Authorization"] = getattr(CaseData, "token_value")
        expected = eval(case["expected"])
        row = case["case_id"] + 1
        # 第二步，发送请求，获取结果
        response = self.request.send(url=url, method=method, json=data, headers=headers)
        res = response.json()
        if case["interface"].lower() == "login":
            CaseData.member_id = str(jsonpath.jsonpath(res, "$..id")[0])
            token = jsonpath.jsonpath(res, "$..token")[0]
            token_type = jsonpath.jsonpath(res, "$..token_type")[0]
            CaseData.token_value = token_type + " " + token

        if case["interface"] == "add":
            CaseData.loan_id = str(jsonpath.jsonpath(res, "$..id")[0])

        # 第三步，断言比对预期结果和实际结果
        try:
            self.assertEqual(expected["code"], res["code"])
            # self.assertEqual(expected["msg"], res["msg"])
            self.assertIn(expected["msg"], res["msg"])
        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="未通过")
            log.error("用例{}执行未通过".format(case["title"]))
            log.exception(e)
            raise e

        else:
            self.excel.write_data(row=row, column=8, value="通过")
            log.error("用例{}执行通过".format(case["title"]))

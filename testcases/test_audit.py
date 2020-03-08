import unittest
import os
import jsonpath
from library.ddt import ddt, data
from common.readexcel import ReadExcel
from common.handler_path import DATADIR
from common.handleconfig import conf
from common.handler_requests import SendRequest
from common.handlelog import log
from common.connectdb import DB
from common.handler_data import CaseData, replace_data

case_file = os.path.join(DATADIR, "apicases.xlsx")


@ddt
class TestAudit(unittest.TestCase):
    excel = ReadExcel(case_file, "audit")
    cases = excel.read_data()
    request = SendRequest()
    db = DB()

    @classmethod
    def setUpClass(cls):
        url = conf.get("env", "url") + "/member/login"
        data = {
            "mobile_phone": conf.get("test_data", "admin_phone"),
            "pwd": conf.get("test_data", "admin_pwd")
        }

        headers = eval(conf.get("env", "headers"))
        response = cls.request.send(url=url, method="post", json=data, headers=headers)
        res = response.json()
        token = jsonpath.jsonpath(res, "$..token")[0]
        token_type = jsonpath.jsonpath(res, "$..token_type")[0]
        CaseData.admin_token_value = token_type + " " + token
        CaseData.admin_member_id = str(jsonpath.jsonpath(res, "$..id")[0])

    def setUp(self):
        url = conf.get("env", "url") + "/loan/add"
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(CaseData, "admin_token_value")
        data = {
            "member_id": getattr(CaseData, "admin_member_id"),
            "title": "CC",
            "amount": 300,
            "loan_rate": 5,
            "loan_term": 7,
            "loan_date_type": 1,
            "bidding_days": 3,

        }

        reponse = self.request.send(url=url, method="post", json=data, headers=headers)
        res = reponse.json()
        CaseData.loan_id = str(jsonpath.jsonpath(res, "$..id")[0])

    @data(*cases)
    def test_audit(self, case):
        # 第一步，准备用例数据
        url = conf.get("env", "url") + case["url"]
        method = case["method"]
        # 替换参数中的用户ID
        # case["data"] = case["data"].replace("#loan_id#", self.loan_id)
        case["data"] = replace_data(case["data"])
        data = eval(case["data"])
        # data = eval(case["data"])
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(CaseData, "admin_token_value")
        expected = eval(case["expected"])
        row = case["case_id"] + 1

        # 第二步，发送请求，获取结果
        response = self.request.send(url=url, method=method, json=data, headers=headers)
        res = response.json()
        if res["code"] == 0 and case["title"] == "审核通过":
            CaseData.pass_loan_id = str(data["loan_id"])

        # 第三步，断言比对预期结果和实际结果
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            if case["check_sql"]:
                sql = replace_data(case["check_sql"])
                status = self.db.find_one(sql)["status"]
                self.assertEqual(expected["status"], status)


        except AssertionError as e:
            print("预期结果", expected)
            print("实际结果", res)
            self.excel.write_data(row=row, column=8, value="未通过")
            log.error("用例{}执行未通过".format(case["title"]))
            log.exception(e)
            raise e

        else:
            self.excel.write_data(row=row, column=8, value="通过")
            log.error("用例{}执行通过".format(case["title"]))

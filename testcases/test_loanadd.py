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
from common.connectdb import DB

case_file = os.path.join(DATADIR, "apicases.xlsx")


@ddt
class TestAdd(unittest.TestCase):
    excel = ReadExcel(case_file, "add")
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
        # member_id = jsonpath.jsonpath(res, "$..id")[0]

        CaseData.admin_token_value = token_type + " " + token
        # CaseData.admin_member_id = str(member_id)
        CaseData.admin_member_id = str(jsonpath.jsonpath(res, "$..id")[0])

    @data(*cases)
    def test_add(self, case):
        # 第一步，准备用例数据
        url = conf.get("env", "url") + case["url"]
        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(CaseData, "admin_token_value")
        data = eval(replace_data(case["data"]))
        expected = eval(case["expected"])
        method = case["method"]
        row = case["case_id"] + 1
        # 第二步，发送请求，获取结果
        response = self.request.send(url=url, method=method, json=data, headers=headers)
        res = response.json()

        # 第三步，断言比对预期结果和实际结果
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            # 判断是否需要sql校验
            if case["check_sql"]:
                # 查询当前用户的member_id
                sql = "SELECT member_id FROM futureloan.loan WHERE member_id={}".format(data["member_id"])
                add1 = self.db.find_one(sql)["member_id"]
                # load_id = self.db.find_one(sql)["id"]
                # print(load_id)
                self.assertEqual(add1, data["member_id"])

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

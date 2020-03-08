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
from decimal import Decimal
from common.handler_data import CaseData, replace_data
from common.handle_sign import HandleSign

case_file = os.path.join(DATADIR, "apicases.xlsx")


@ddt
class TestRecharge(unittest.TestCase):
    excel = ReadExcel(case_file, "recharge")
    cases = excel.read_data()
    request = SendRequest()
    db = DB()

    @classmethod
    def setUpClass(cls):
        url = conf.get("env", "url") + "/member/login"
        data = {
            "mobile_phone": conf.get("test_data", "phone"),
            "pwd": conf.get("test_data", "pwd")
        }

        headers = eval(conf.get("env", "headers"))
        response = cls.request.send(url=url, method="post", json=data, headers=headers)
        res = response.json()
        token = jsonpath.jsonpath(res, "$..token")[0]
        token_type = jsonpath.jsonpath(res, "$..token_type")[0]
        CaseData.token = token
        CaseData.token_value = token_type + " " + token
        CaseData.member_id = str(jsonpath.jsonpath(res, "$..id")[0])

    @data(*cases)
    def test_recharge(self, case):
        # 第一步，准备用例数据
        url = conf.get("env", "url") + case["url"]
        method = case["method"]
        # 替换参数中的用户ID
        # case["data"] = case["data"].replace("#member_id#", str(self.member_id))
        case["data"] = replace_data(case["data"])
        data = eval(case["data"])
        # 在请求体中加入时间戳和签名
        sign_info = HandleSign.generate_sign(getattr(CaseData, "token"))
        data.update(sign_info)

        headers = eval(conf.get("env", "headers"))
        headers["Authorization"] = getattr(CaseData, "token_value")

        expected = eval(case["expected"])
        row = case["case_id"] + 1
        if case["check_sql"]:
            # 查询当前用户的余额
            sql = "SELECT leave_amount FROM futureloan.member WHERE mobile_phone={}".format(
                conf.get("test_data", "phone"))
            start_money = self.db.find_one(sql)["leave_amount"]

        # 第二步，发送请求，获取结果
        response = self.request.send(url=url, method=method, json=data, headers=headers)
        res = response.json()
        if case["check_sql"]:
            # 查询当前用户的余额
            sql = "SELECT leave_amount FROM futureloan.member WHERE mobile_phone={}".format(
                conf.get("test_data", "phone"))
            end_money = self.db.find_one(sql)["leave_amount"]

        # 第三步，断言比对预期结果和实际结果
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])
            # 判断是否需要sql校验
            if case["check_sql"]:
                self.assertEqual(end_money - start_money, Decimal(str(data["amount"])))

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

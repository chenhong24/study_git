import unittest
import random
import os
from library.ddt import ddt, data
from common.readexcel import ReadExcel
from common.handler_path import DATADIR
from common.handleconfig import conf
from common.handler_requests import SendRequest
from common.handlelog import log
from common.connectdb import DB

case_file = os.path.join(DATADIR, "apicases.xlsx")


@ddt
class TestRegister(unittest.TestCase):
    excel = ReadExcel(case_file, "register")
    cases = excel.read_data()
    request = SendRequest()
    db = DB()

    @data(*cases)
    def test_register(self, case):
        # 第一步，准备用例数据
        url = conf.get("env", "url") + case["url"]
        method = case["method"]
        # 生成一个手机号码
        phone = self.random_phone()
        # 替换用例数据
        case["data"] = case["data"].replace("#phone#", phone)
        data = eval(case["data"])
        headers = eval(conf.get("env", "headers"))
        expected = eval(case["expected"])
        row = case["case_id"] + 1

        # 第二步，发送请求，获取结果
        response = self.request.send(url=url, method=method, json=data, headers=headers)
        res = response.json()
        if case["check_sql"]:
            sql = "SELECT mobile_phone FROM futureloan.member WHERE mobile_phone={}".format(phone)
            user = self.db.find_one(sql)["mobile_phone"]

        # 第三步，断言比对预期结果和实际结果
        try:
            self.assertEqual(expected["code"], res["code"])
            self.assertEqual(expected["msg"], res["msg"])

            if case["check_sql"]:
                self.assertEqual(user, phone)

        except AssertionError as e:
            self.excel.write_data(row=row, column=8, value="未通过")
            log.error("用例{}执行未通过".format(case["title"]))
            log.exception(e)
            raise e
        else:
            self.excel.write_data(row=row, column=8, value="通过")
            log.error("用例{}执行通过".format(case["title"]))

    def random_phone(self):
        phone = "136"
        n = random.randint(100000000, 999999999)
        phone += str(n)[1:]
        return phone

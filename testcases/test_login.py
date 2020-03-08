import unittest
import os
from library.ddt import ddt, data
from common.readexcel import ReadExcel
from common.handler_path import DATADIR
from common.handleconfig import conf
from common.handler_requests import SendRequest
from common.handlelog import log

case_file = os.path.join(DATADIR, "apicases.xlsx")


@ddt
class TestLogin(unittest.TestCase):
    excel = ReadExcel(case_file, "login")
    cases = excel.read_data()
    request = SendRequest()

    @data(*cases)
    def test_login(self, case):
        # 第一步，准备用例数据
        url = conf.get("env", "url") + case["url"]
        method = case["method"]
        data = eval(case["data"])
        headers = eval(conf.get("env", "headers"))
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
            log.error("用例{}执行未通过".format(case["title"]))
            log.exception(e)
            raise e

        else:
            self.excel.write_data(row=row, column=8, value="通过")
            log.error("用例{}执行通过".format(case["title"]))


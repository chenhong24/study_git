import unittest
import os
from HTMLTestRunnerNew import HTMLTestRunner
from common.handler_path import CASEDIR, REPORTDIR
from common.handler_email import send_email
import datetime


date = datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")

suite = unittest.TestSuite()
loader = unittest.TestLoader()
suite.addTest(loader.discover(CASEDIR))
# from testcases import test_recharge
#
# suite.addTest(loader.loadTestsFromModule(test_recharge))
report_file = os.path.join(REPORTDIR, date + "report1.html")

runner = HTMLTestRunner(stream=open(report_file, "wb"),
                        description="接口测试报告",
                        title="testreport",
                        tester="CCCC"
                        )
runner.run(suite)
send_email(report_file, "CC")

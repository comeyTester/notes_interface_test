import unittest
from BeautifulReport import BeautifulReport
from common.getProjectPath import *

testLoader = unittest.TestLoader()


# suite = testLoader.discover("./testCase", "test_set*.py")

# runner = unittest.TextTestRunner()
# runner.run(suite)


def run(test_suite):
    # 定义输出的文件位置和名字
    filename = "report.html"
    result = BeautifulReport(test_suite)
    result.report(filename=filename, description='测试报告')


if __name__ == '__main__':
    pattern = 'all'  # all执行全量用例，smoking冒烟用例
    if pattern == 'all':
        suite = testLoader.discover("./testCase", "test*.py")
    else:
        suite = testLoader.discover("./testCase", "test_level1*.py")
    run(suite)

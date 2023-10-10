import os

"""
常量模块，
获取项目项目目录的路径，保存

项目路径：
用例类所在路径：
配置文件的路径：
用例数据的路径：
日志文件的路径：
测试报告的路径：

"""


# 项目目录路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 通用的公共方法存放的地址
COMMON_DIR = os.path.join(BASE_DIR, 'common')

# 通用的公共方法存放的地址
BUSINESS_COMMON_DIR = os.path.join(BASE_DIR, 'BusinessCommon')

# 测试用例所在的目录路径
CASES_DIR = os.path.join(BASE_DIR, 'testCase')

# 测试报告所在的目录路径
REPORT_DIR = os.path.join(BASE_DIR, 'testReports')

# 日志文件所在的目录路径
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# 配置文件所在的目录
CONF_DIR = os.path.join(BASE_DIR, 'envConfig')

# 线上配置文件所在的目录
ONLINE_CONF_DIR = os.path.join(CONF_DIR, 'Online')

# 配置文件所在的目录
OFFLINE_CONF_DIR = os.path.join(CONF_DIR, 'Offline')

# 用例数据所在的目录
DATA_DIR = os.path.join(BASE_DIR, 'testData')

# 测试套件所在的目录
SUITE_DIR = os.path.join(BASE_DIR, 'testSuite')


if __name__ == '__main__':
    print(CONF_DIR)
    print(ONLINE_CONF_DIR)



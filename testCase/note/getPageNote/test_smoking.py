import json
import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.yamlOperation import ReadYaml
from common.caseLogsMethod import info, step, class_case_log, func_case_log
from businessCommon.apiRe import ApiRe
from businessCommon.businessNote import BusinessNote


@class_case_log
class GetPageNoteSmoking(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('testData.yml','getPageNote',)
    host = envConfig['host']
    path = apiConfig['path']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    BusinessNote = BusinessNote()

    def setUp(self) -> None:
        BusinessNote.clear_note(self.user_id, self.sid)

    # @func_case_log
    def testCase01_major(self):
        """获取便签首页内容 主流程"""
        step("STEP:前置步骤：给用户A添加1条便签数据")
        note_ids = BusinessNote.multi_set_note(1, self.sid, self.user_id)
        start_index = 0
        rows = 0
        url = self.url.format(userid=self.user_id, startindex=start_index, rows=rows)
        # print(url)
        step("STEP:获取首页便签列表")
        res = self.apiRe.note_get(url, self.sid)
        print(res.json())
        self.assertEqual(200, res.status_code, msg='状态码错误')
        expect = {'responseTime': int, 'webNotes': [
            {
                'noteId': note_ids[0],
                'createTime': int,
                'star': int,
                'remindTime': int,
                'remindType': int,
                'infoVersion': int,
                'infoUpdateTime': int,
                'groupId': None,
                'title': str,
                'summary': str,
                'thumbnail': None,
                'contentVersion': int,
                'contentUpdateTime': int,

            }
        ]
                  }
        info(f'expect body:{expect}')
        step("期望:1、接口返回状态码: 200 \n2、接口返回体对齐文档 \n3、返回一条便签数据")
        CheckTools().check_output(expect, res.json())

    def testCase02_sid(self):
        """获取便签首页内容 wps_sid不正确 """
        start_index = 0
        rows = 0
        url = self.url.format(userid=self.user_id, startindex=start_index, rows=rows)
        # print(url)
        step("STEP:获取首页便签列表")
        sid = "abcd"
        res = self.apiRe.note_get(url, sid)
        print(res.json())
        self.assertEqual(401, res.status_code, msg='状态码错误')
        expect = {'errorCode': -2010,
                  'errorMsg': str
                  }
        info(f'expect body:{expect}')
        step("期望:1、接口返回状态码: 401")
        CheckTools().check_output(expect, res.json())

    def testCase03_user_id(self):
        """获取便签首页内容 user_id不正确 """
        start_index = 0
        rows = 0
        user_id = "123"
        url = self.url.format(userid=user_id, startindex=start_index, rows=rows)
        # print(url)
        step("STEP:获取首页便签列表")
        sid = "abcd"
        res = self.apiRe.note_get(url, sid)
        print(res.json())
        self.assertEqual(401, res.status_code, msg='状态码错误')
        expect = {'errorCode': -2010,
                  'errorMsg': str
                  }
        info(f'expect body:{expect}')
        step("期望:1、接口返回状态码: 401")
        CheckTools().check_output(expect, res.json())

if __name__ == '__main__':
    unittest.main()

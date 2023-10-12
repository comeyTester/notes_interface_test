import json
import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.yamlOperation import ReadYaml
from common.caseLogsMethod import info, step, class_case_log, func_case_log
from businessCommon.apiRe import ApiRe
from copy import deepcopy
from businessCommon.businessNote import BusinessNote


@class_case_log
class GetNoteGroupSmoking(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('testData.yml', 'getNoteGroup')
    host = envConfig['host']
    path = apiConfig['path']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    BusinessNote = BusinessNote()

    def setUp(self) -> None:
        pass

    # @func_case_log
    def testCase01_major(self):
        """获取分组列表 主流程"""
        body = {}
        step('STEP:获取分组列表')
        set_note_content_res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, set_note_content_res.status_code, msg='状态码错误')
        expect = {
            'requestTime': int,
            'noteGroups': [{
                'userId': str,
                'groupId': str,
                'groupName': str,
                'order': int,
                'valid': int,
                'updateTime':int

            }



        ]

            }
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, set_note_content_res.json())

    def testCase02_user_id(self):
        """获取分组列表 user_id不正确"""
        body = {}
        step('STEP:获取分组列表')
        user_id= '123'
        set_note_content_res = self.apiRe.note_post(self.url, user_id, self.sid, body)
        self.assertEqual(412, set_note_content_res.status_code, msg='状态码错误')
        expect = {'errorCode': -1011, 'errorMsg': 'user change!'}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, set_note_content_res.json())

    def testCase03_sid(self):
        """获取分组列表 sid不正确"""
        body = {}
        step('STEP:获取分组列表')
        sid = 'abc'
        set_note_content_res = self.apiRe.note_post(self.url, self.user_id, sid, body)
        self.assertEqual(401, set_note_content_res.status_code, msg='状态码错误')
        expect = {'errorCode': -2010, 'errorMsg': ''}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, set_note_content_res.json())


if __name__ == '__main__':
    unittest.main()

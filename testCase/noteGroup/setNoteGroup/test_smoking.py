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
class SetNoteGroupSmoking(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('testData.yml', 'setNoteGroup')
    host = envConfig['host']
    path = apiConfig['path']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    must_key = apiConfig['must_key']
    apiRe = ApiRe()
    BusinessNote = BusinessNote()
    base_body = {
        'groupId': "groupId",
        'groupName': 'test_groupName',
        'order': 0
    }

    # @func_case_log
    def testCase01_major(self):
        """新增分组 主流程"""

        step('STEP:获取便签主体版本')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        body = deepcopy(self.base_body)
        body['groupId'] = group_id
        step('STEP:新增分组')
        set_note_content_res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, set_note_content_res.status_code, msg='状态码错误')
        expect = {'responseTime': int, 'updateTime': int}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, set_note_content_res.json())

    @parameterized.expand(must_key)
    def testCase02_must_input(self, dic):
        """新增分组 必填项校验"""
        step('STEP:获取便签主体版本')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        body = deepcopy(self.base_body)
        body['groupId'] = group_id
        body.pop(dic['key'])
        step('STEP:新增分组')
        set_note_content_res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        if dic['code'] == 500:
            self.assertEqual(dic['code'], set_note_content_res.status_code, msg='状态码错误')
            expect = {'errorCode': -7, 'errorMsg': '参数不合法！'}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, set_note_content_res.json())
        else:
            self.assertEqual(dic['code'], set_note_content_res.status_code, msg='状态码错误')
            expect = {'responseTime': int, 'updateTime': int}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, set_note_content_res.json())

    def testCase03_user_id(self):
        """新增分组  userid不正确"""
        step('STEP:获取便签主体版本')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        body = deepcopy(self.base_body)
        body['groupId'] = group_id
        step('STEP:新增分组')
        user_id = '123'
        set_note_content_res = self.apiRe.note_post(self.url, user_id, self.sid, body)
        self.assertEqual(412, set_note_content_res.status_code, msg='状态码错误')
        expect = {'errorCode': -1011, 'errorMsg': 'user change!'}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, set_note_content_res.json())

    def testCase04_sid(self):
        """新增分组  sid不正确"""
        step('STEP:获取便签主体版本')
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        body = deepcopy(self.base_body)
        body['groupId'] = group_id
        step('STEP:新增分组')
        sid = 'abc'
        set_note_content_res = self.apiRe.note_post(self.url, self.user_id,sid, body)
        self.assertEqual(401, set_note_content_res.status_code, msg='状态码错误')
        expect = {'errorCode': -2010, 'errorMsg': str}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, set_note_content_res.json())


if __name__ == '__main__':
    unittest.main()

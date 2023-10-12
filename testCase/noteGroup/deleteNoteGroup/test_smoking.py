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
class DeleteNoteGroupSmoking(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('testData.yml', 'deleteNoteGroup')
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
        """删除分组 主流程"""

        step('STEP:新增分组')
        group_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'groupId': group_id
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码错误')
        expect = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())

    def testCase02_must_input(self, dic):
        """删除分组 必填项校验"""
        # info(f'必填项校验的字段{dic}')
        step('STEP:新增分组')
        group_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'groupId': group_id
        }
        body.pop('groupId')
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码错误')
        expect = {'errorCode': int, 'errorMsg': str}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())

    def testCase03_user_id(self):
        """删除分组  userid不正确"""
        step('STEP:新增分组')
        group_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'groupId': group_id
        }
        body.pop('groupId')
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码错误')
        expect = {'errorCode': int, 'errorMsg': str}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())

    def testCase04_sid(self):
        """删除分组  sid不正确"""
        step('STEP:新增分组')
        group_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'groupId': group_id
        }
        body.pop('groupId')
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码错误')
        expect = {'errorCode': int, 'errorMsg': str}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())


if __name__ == '__main__':
    unittest.main()

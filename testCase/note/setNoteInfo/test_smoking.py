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
from copy import deepcopy


@class_case_log
class SetNoteInfoSmoking(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    host = envConfig['host']
    path = apiConfig['setNoteInfo']['path']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    base_body = {
        'noteId': 'note_id',
        'star': 0,
        'remindTime': 0,
        'remindType': 0
    }

    # @func_case_log
    def testCase01_major(self):
        """上传/更新便签主体 主流程"""

        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        # note_info_body = {
        #     'noteId': note_id,
        #     'star': 0,
        #     'remindTime': 0,
        #     'remindType': 0,
        #     'groupId':  #组ID
        # }
        body = deepcopy(self.base_body)
        body['noteId'] = note_id
        step("请求新增便签主体接口")
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码错误')
        expect = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())
        step("验证新增一条普通便签主体（无法检查数据源）？？？")

    def testCase02_must_input(self):
        """上传/更新便签主体 必填项校验noteId"""

        body = deepcopy(self.base_body)
        body.pop('noteId')
        step("请求新增便签主体接口")
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码错误')
        expect = {'errorCode': int, 'errorMsg': str}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())

    def testCase03_sid(self):
        """上传/更新便签主体 wps_sid不正确"""

        body = deepcopy(self.base_body)
        body.pop('noteId')
        step("请求新增便签主体接口")
        sid = "abcd"
        res = self.apiRe.note_post(self.url, self.user_id, sid, body)
        self.assertEqual(500, res.status_code, msg='状态码错误')
        expect = {'errorCode': int, 'errorMsg': str}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())

    def testCase04_user_id(self):
        """上传/更新便签主体 user_id不正确"""

        body = deepcopy(self.base_body)
        body.pop('noteId')
        step("请求新增便签主体接口")
        user_id = "123"
        res = self.apiRe.note_post(self.url, user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码错误')
        expect = {'errorCode': int, 'errorMsg': str}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())


if __name__ == '__main__':
    unittest.main()

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
class GetNotesInGroupSmoking(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('testData.yml', 'getNotesInGroup')
    host = envConfig['host']
    path = apiConfig['path']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    BusinessNote = BusinessNote()
    base_body = {
        'groupId': "groupId",
        'startIndex': 0,
        'rows': 10
    }

    def setUp(self) -> None:
        pass

    # @func_case_log
    def testCase01_major(self):
        """查看分组下便签 主流程"""

        step('STEP:新增一个分组')
        group_ids = BusinessNote.multi_set_note_group(1, self.user_id, self.sid)

        step("STEP:新增便签绑定分组")
        group_id = group_ids[0]
        note_id = BusinessNote.set_note_has_group_id(group_id, self.user_id, self.sid)

        body = deepcopy(self.base_body)
        body['groupId'] = group_id
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码错误')
        expect = {
            'responseTime': int,
            'webNotes': [
                {
                    'noteId': note_id,
                    'createTime': int,
                    'star': int,
                    'remindTime': int,
                    'remindType': int,
                    'infoVersion': int,
                    'infoUpdateTime': int,
                    'groupId': group_id,
                    'title': str,
                    'summary': str,
                    'thumbnail': None,
                    'contentVersion': int,
                    'contentUpdateTime': int
                }
            ]
        }
        CheckTools().check_output(expect, res.json())

    def testCase02_must_input(self):
        """查看分组下便签 必填项校验"""
        step('STEP:新增一个分组')
        group_ids = BusinessNote.multi_set_note_group(1, self.user_id, self.sid)

        step("STEP:新增便签绑定分组")
        group_id = group_ids[0]
        note_id = BusinessNote.set_note_has_group_id(group_id, self.user_id, self.sid)

        body = deepcopy(self.base_body)
        body['groupId'] = group_id
        body.pop('groupId')
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码错误')
        expect = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        CheckTools().check_output(expect, res.json())

    def testCase03_user_id(self):
        """查看分组下便签  userid不正确"""
        step('STEP:新增一个分组')
        group_ids = BusinessNote.multi_set_note_group(1, self.user_id, self.sid)

        step("STEP:新增便签绑定分组")
        group_id = group_ids[0]
        note_id = BusinessNote.set_note_has_group_id(group_id, self.user_id, self.sid)

        body = deepcopy(self.base_body)
        body['groupId'] = group_id
        user_id = '123'
        res = self.apiRe.note_post(self.url, user_id, self.sid, body)
        self.assertEqual(412, res.status_code, msg='状态码错误')
        expect = {'errorCode': -1011, 'errorMsg': 'user change!'}
        CheckTools().check_output(expect, res.json())

    def testCase04_sid(self):
        """查看分组下便签  sid不正确"""
        step('STEP:新增一个分组')
        group_ids = BusinessNote.multi_set_note_group(1, self.user_id, self.sid)

        step("STEP:新增便签绑定分组")
        group_id = group_ids[0]
        note_id = BusinessNote.set_note_has_group_id(group_id, self.user_id, self.sid)
        body = deepcopy(self.base_body)
        body['groupId'] = group_id
        sid = 'abc'
        res = self.apiRe.note_post(self.url, self.user_id, sid, body)
        self.assertEqual(401, res.status_code, msg='状态码错误')
        expect = {'errorCode': -2010, 'errorMsg': ''}
        CheckTools().check_output(expect, res.json())


if __name__ == '__main__':
    unittest.main()

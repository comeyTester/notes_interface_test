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
class CleanRecycleBinSmoking(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('testData.yml', 'cleanRecycleBin')
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
        """清空回收站 主流程"""
        step('STEP:新增一条便签')
        note_ids = BusinessNote.multi_set_note(1, self.sid, self.user_id)
        step('STEP:删除一条便签')
        note_id = note_ids[0]
        BusinessNote.delete_note(note_id, self.user_id, self.sid)
        step('STEP:清空回收站')
        body = {
            'noteIds': [note_id]
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码错误')
        expect = {'responseTime': int}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())
        step('STEP:验证便签首页列表数据为空')
        note_ids = BusinessNote.get_note_ids(self.user_id, self.sid)
        self.assertEqual(0, len(note_ids))

    def testCase02_must_input(self):
        """清空回收站 必填项校验"""
        step('STEP:新增一条便签')
        note_ids = BusinessNote.multi_set_note(1, self.sid, self.user_id)
        step('STEP:删除一条便签')
        note_id = note_ids[0]
        BusinessNote.delete_note(note_id, self.user_id, self.sid)
        step('STEP:清空回收站')
        body = {
            'noteIds': [note_id]
        }
        body.pop('noteIds')
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码错误')
        expect = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())

    def testCase03_user_id(self):
        """清空回收站  userid不正确"""
        step('STEP:新增一条便签')
        note_ids = BusinessNote.multi_set_note(1, self.sid, self.user_id)
        step('STEP:删除一条便签')
        note_id = note_ids[0]
        BusinessNote.delete_note(note_id, self.user_id, self.sid)
        step('STEP:清空回收站')
        body = {
            'noteIds': [note_id]
        }
        user_id = '123'
        res = self.apiRe.note_post(self.url, user_id, self.sid, body)
        self.assertEqual(412, res.status_code, msg='状态码错误')
        expect = {'errorCode': -1011, 'errorMsg': 'user change!'}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())


    def testCase04_sid(self):
        """清空回收站  sid不正确"""
        step('STEP:新增一条便签')
        note_ids = BusinessNote.multi_set_note(1, self.sid, self.user_id)
        step('STEP:删除一条便签')
        note_id = note_ids[0]
        BusinessNote.delete_note(note_id, self.user_id, self.sid)
        step('STEP:清空回收站')
        body = {
            'noteIds': [note_id]
        }
        sid = 'abc'
        res = self.apiRe.note_post(self.url, self.user_id, sid, body)
        self.assertEqual(401, res.status_code, msg='状态码错误')
        expect = {'errorCode': -2010, 'errorMsg': ''}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())


if __name__ == '__main__':
    unittest.main()

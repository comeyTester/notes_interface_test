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
class GetRecycleBinListSmoking(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('testData.yml', 'getRecycleBinList')
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
        """查看回收站下便签列表 主流程"""

        step('STEP:新增1条便签')
        note_ids = BusinessNote.multi_set_note(1, self.sid, self.user_id)
        step('STEP:删除1条便签')
        note_id = note_ids[0]
        BusinessNote.delete_note(note_id, self.user_id, self.sid)
        step('STEP:获取回收站下的便签列表')
        start_index = 0
        rows = 0
        url = self.url.format(userid=self.user_id, startindex=start_index, rows=rows)
        res = self.apiRe.note_get(url, self.sid)
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
                    'groupId': None,
                    'title': str,
                    'summary': str,
                    'thumbnail': None,
                    'contentVersion': int,
                    'contentUpdateTime': int
                }

            ]
        }
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())
    #
    # @parameterized.expand(must_key)
    # def testCase02_must_input(self, dic):
    #     """新增分组 必填项校验"""
    #     step('STEP:获取便签主体版本')
    #     group_id = str(int(time.time() * 1000)) + '_test_groupId'
    #     body = deepcopy(self.base_body)
    #     body['groupId'] = group_id
    #     body.pop(dic['key'])
    #     step('STEP:新增分组')
    #     res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
    #     if dic['code'] == 500:
    #         self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
    #         expect = {'errorCode': -7, 'errorMsg': '参数不合法！'}
    #         info(f'expect body:{expect}')
    #         CheckTools().check_output(expect, res.json())
    #     else:
    #         self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
    #         expect = {'responseTime': int, 'updateTime': int}
    #         info(f'expect body:{expect}')
    #         CheckTools().check_output(expect, res.json())
    #
    # def testCase03_user_id(self):
    #     """新增分组  userid不正确"""
    #     step('STEP:获取便签主体版本')
    #     group_id = str(int(time.time() * 1000)) + '_test_groupId'
    #     body = deepcopy(self.base_body)
    #     body['groupId'] = group_id
    #     step('STEP:新增分组')
    #     user_id = '123'
    #     res = self.apiRe.note_post(self.url, user_id, self.sid, body)
    #     self.assertEqual(412, res.status_code, msg='状态码错误')
    #     expect = {'errorCode': -1011, 'errorMsg': 'user change!'}
    #     info(f'expect body:{expect}')
    #     CheckTools().check_output(expect, res.json())
    #
    # def testCase04_sid(self):
    #     """新增分组  sid不正确"""
    #     step('STEP:获取便签主体版本')
    #     group_id = str(int(time.time() * 1000)) + '_test_groupId'
    #     body = deepcopy(self.base_body)
    #     body['groupId'] = group_id
    #     step('STEP:新增分组')
    #     sid = 'abc'
    #     res = self.apiRe.note_post(self.url, self.user_id, sid, body)
    #     self.assertEqual(401, res.status_code, msg='状态码错误')
    #     expect = {'errorCode': -2010, 'errorMsg': str}
    #     info(f'expect body:{expect}')
    #     CheckTools().check_output(expect, res.json())
    #


if __name__ == '__main__':
    unittest.main()

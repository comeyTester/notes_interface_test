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
                    'infoVersion':int,
                    'infoUpdateTime': int,
                    'groupId': group_id,
                    'title': str,
                    'summary': str,
                    'thumbnail': str,
                    'contentVersion': int
                }
            ]
        }
        CheckTools().check_output(expect, res.json())

    #
    # @parameterized.expand(must_key)
    # def testCase02_must_input(self, dic):
    #     """上传/更新便签内容 必填项校验"""
    #     # info(f'必填项校验的字段{dic}')
    #     step('STEP:获取便签主体版本')
    #
    #     note_id = str(int(time.time() * 1000)) + '_test_noteId'
    #     body = {
    #         'noteId': note_id
    #     }
    #     res = self.apiRe.note_post(self.note_info_url, self.user_id, self.sid, body)
    #     self.assertEqual(200, res.status_code, msg='状态码错误')
    #     info_version = res.json()['infoVersion']
    #     step(f'接口关联参数info_version:{info_version}')
    #
    #     body = deepcopy(self.base_body)
    #     body['noteId'] = note_id
    #     body['localContentVersion'] = info_version
    #     body.pop(dic['key'])
    #     step('STEP:新增便签内容')
    #     set_note_content_res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
    #     if dic['code'] == 200:
    #         self.assertEqual(dic['code'], set_note_content_res.status_code, msg='状态码错误')
    #         expect = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
    #         info(f'expect body:{expect}')
    #         CheckTools().check_output(expect, set_note_content_res.json())
    #     else:
    #         self.assertEqual(dic['code'], set_note_content_res.status_code, msg='状态码错误')
    #         expect = {'errorCode': int, 'errorMsg': str}
    #         info(f'expect body:{expect}')
    #         CheckTools().check_output(expect, set_note_content_res.json())
    #
    # def testCase03_user_id(self):
    #     """上传/更新便签内容  userid不正确"""
    #     step('STEP:获取便签主体版本')
    #
    #     note_id = str(int(time.time() * 1000)) + '_test_noteId'
    #     body = {
    #         'noteId': note_id
    #     }
    #     res = self.apiRe.note_post(self.note_info_url, self.user_id, self.sid, body)
    #     self.assertEqual(200, res.status_code, msg='状态码错误')
    #     info_version = res.json()['infoVersion']
    #     step(f'接口关联参数info_version:{info_version}')
    #
    #     body = deepcopy(self.base_body)
    #     body['noteId'] = note_id
    #     body['localContentVersion'] = info_version
    #     step('STEP:新增便签内容')
    #     user_id = '123'
    #     set_note_content_res = self.apiRe.note_post(self.url, user_id, self.sid, body)
    #     self.assertEqual(412, set_note_content_res.status_code, msg='状态码错误')
    #     expect = {'errorCode': int, 'errorMsg': str}
    #     info(f'expect body:{expect}')
    #     CheckTools().check_output(expect, set_note_content_res.json())
    #
    # def testCase04_sid(self):
    #     """上传/更新便签内容  sid不正确"""
    #     step('STEP:获取便签主体版本')
    #
    #     note_id = str(int(time.time() * 1000)) + '_test_noteId'
    #     body = {
    #         'noteId': note_id
    #     }
    #     res = self.apiRe.note_post(self.note_info_url, self.user_id, self.sid, body)
    #     self.assertEqual(200, res.status_code, msg='状态码错误')
    #     info_version = res.json()['infoVersion']
    #     step(f'接口关联参数info_version:{info_version}')
    #
    #     body = deepcopy(self.base_body)
    #     body['noteId'] = note_id
    #     body['localContentVersion'] = info_version
    #     step('STEP:新增便签内容')
    #     sid = 'abc'
    #     set_note_content_res = self.apiRe.note_post(self.url, self.user_id, sid, body)
    #     self.assertEqual(401, set_note_content_res.status_code, msg='状态码错误')
    #     expect = {'errorCode': int, 'errorMsg': str}
    #     info(f'expect body:{expect}')
    #     CheckTools().check_output(expect, set_note_content_res.json())


if __name__ == '__main__':
    unittest.main()

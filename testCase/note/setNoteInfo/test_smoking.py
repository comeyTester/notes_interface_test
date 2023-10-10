import json
import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.yamlOperation import ReadYaml
from common.caseLogsMethod import info, class_case_log, func_case_log
from businessCommon.apiRe import ApiRe
from businessCommon.businessNote import BusinessNote


@class_case_log
class SetNoteInfoSmoking(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    host = envConfig['host']
    path = apiConfig['setNoteContent']['path']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    note_info_path = apiConfig['setNoteInfo']['path']
    note_info_url = host + note_info_path
    must_key = apiConfig['setNoteContent']['must_key']
    apiRe = ApiRe()

    # @func_case_log
    def testCase01_major(self):
        """上传/更新便签内容 主流程"""

        info('STEP:获取便签主体版本')
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        note_info_body = {
            'noteId': note_id
        }
        res = self.apiRe.note_post(self.note_info_url, self.user_id, self.sid, note_info_body)
        self.assertEqual(200, res.status_code, msg='状态码错误')
        info_version = res.json()['infoVersion']
        info(f'接口关联参数info_version:{info_version}')

        set_note_content_body = {
            'noteId': note_id,
            'title': 'test_title',
            'summary': 'test_summary',
            'body': 'test_body',
            'localContentVersion': info_version,
            'BodyType': 0
        }
        info('STEP:新增便签内容')
        set_note_content_res = self.apiRe.note_post(self.url, self.user_id, self.sid, set_note_content_body)
        self.assertEqual(200, set_note_content_res.status_code, msg='状态码错误')
        expect = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, set_note_content_res.json())

    @parameterized.expand(must_key)
    def testCase02_must_input(self, dic):
        """上传/更新便签内容 必填项校验"""
        # info(f'必填项校验的字段{dic}')
        info('STEP:获取便签主体版本')

        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id
        }
        res = self.apiRe.note_post(self.note_info_url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码错误')
        info_version = res.json()['infoVersion']
        info(f'接口关联参数info_version:{info_version}')

        set_note_content_body = {
            'noteId': note_id,
            'title': 'test_title',
            'summary': 'test_summary',
            'body': 'test_body',
            'localContentVersion': info_version,
            'BodyType': 0
        }
        set_note_content_body.pop(dic['key'])
        info('STEP:新增便签内容')
        set_note_content_res = self.apiRe.note_post(self.url, self.user_id, self.sid, set_note_content_body)
        if dic['code'] == 200:
            self.assertEqual(dic['code'], set_note_content_res.status_code, msg='状态码错误')
            expect = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, set_note_content_res.json())
        else:
            self.assertEqual(dic['code'], set_note_content_res.status_code, msg='状态码错误')
            expect = {'errorCode': int, 'errorMsg': str}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, set_note_content_res.json())


if __name__ == '__main__':
    unittest.main()

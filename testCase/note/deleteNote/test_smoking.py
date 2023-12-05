
import unittest
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.yamlOperation import ReadYaml
from common.caseLogsMethod import info, step , class_case_log, func_case_log
from businessCommon.apiRe import ApiRe
from businessCommon.businessNote import BusinessNote


@class_case_log
class DeleteNoteSmoking(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('testData.yml', 'deleteNote')
    host = envConfig['host']
    path = apiConfig['path']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    BusinessNote = BusinessNote()


    def setUp(self) -> None:
        BusinessNote.clear_note(self.user_id, self.sid)

    def testCase01_major(self):
        """删除便签 主流程"""
        step('STEP:新增一条便签内容')
        note_ids = BusinessNote.multi_set_note(1, self.sid, self.user_id)
        body = {
            'noteId': note_ids[0]
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码错误')
        expect = {'responseTime': int}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())
        step('STEP:验证获取便签首页的数据为空')
        note_id = BusinessNote.get_note_ids(self.user_id, self.sid)
        # print(note_id)
        self.assertEqual(0, len(note_id))

    def testCase02_must_key(self):
        """删除便签 noteId必填项校验"""
        step('STEP:新增一条便签内容')
        note_ids = BusinessNote.multi_set_note(1, self.sid, self.user_id)

        body = {
            'noteId': note_ids[0]
        }
        body.pop('noteId')
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码错误')
        expect = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())


    def testCase03_sid(self):
        """删除便签 sid不正确"""
        step('STEP:新增一条便签内容')
        note_ids = BusinessNote.multi_set_note(1, self.sid, self.user_id)

        body = {
            'noteId': note_ids[0]
        }
        body.pop('noteId')
        sid = 'abc'
        res = self.apiRe.note_post(self.url, self.user_id, sid, body)
        self.assertEqual(500, res.status_code, msg='状态码错误')
        expect = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())

    def testCase04_user_id(self):
        """删除便签 user_id不正确"""
        step('STEP:新增一条便签内容')
        note_ids = BusinessNote.multi_set_note(1, self.sid, self.user_id)

        body = {
            'noteId': note_ids[0]
        }
        body.pop('noteId')
        user_id = '123'
        res = self.apiRe.note_post(self.url, user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码错误')
        expect = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())


if __name__ == '__main__':
    unittest.main()


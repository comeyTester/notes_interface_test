import unittest
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.yamlOperation import ReadYaml
from common.caseLogsMethod import info, step, class_case_log, func_case_log
from businessCommon.apiRe import ApiRe
from businessCommon.businessNote import BusinessNote


@class_case_log
class GetNoteBodySmoking(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('testData.yml', 'getNoteBody')
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
        """获取便签主体内容 主流程"""
        step('STEP:新增一条便签内容')
        note_id = BusinessNote.multi_set_note(1, self.sid, self.user_id)

        body = {
            'noteIds': note_id
        }
        step("STEP:获取便签主体内容")
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码错误')
        print(len(res.json()["noteBodies"]))
        expect = {'responseTime': int,
                  'noteBodies': [
                      {
                          'summary': str,
                          'noteId': note_id[0],
                          'infoNoteId': str,
                          'bodyType': int,
                          'body': str,
                          'contentVersion': int,
                          'contentUpdateTime': int,
                          'title': str,
                          'valid': int
                      }
                  ]}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())

    def testCase02_must_key(self):
        """获取便签主体内容 note_id必填项校验"""
        step('STEP:新增一条便签内容')
        note_id = BusinessNote.multi_set_note(1, self.sid, self.user_id)

        body = {
            'noteIds': note_id
        }
        body.pop('noteIds')
        step("STEP:获取便签主体内容")
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码错误')
        expect = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())

    def testCase03_sid(self):
        """获取便签主体内容 sid不正确 """
        step('STEP:新增一条便签内容')
        note_id = BusinessNote.multi_set_note(1, self.sid, self.user_id)

        body = {
            'noteIds': note_id
        }
        sid = 'abc'
        step("STEP:获取便签主体内容")
        res = self.apiRe.note_post(self.url, self.user_id, sid, body)
        self.assertEqual(401, res.status_code, msg='状态码错误')
        expect = {'errorCode': int, 'errorMsg': str}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())

    def testCase04_user_id(self):
        """获取便签主体内容 user_id不正确"""
        step('STEP:新增一条便签内容')
        note_id = BusinessNote.multi_set_note(1, self.sid, self.user_id)

        body = {
            'noteIds': note_id
        }
        body.pop('noteIds')
        step("STEP:获取便签主体内容")
        user_id = '123'
        res = self.apiRe.note_post(self.url, user_id, self.sid, body)
        self.assertEqual(500, res.status_code, msg='状态码错误')
        expect = {'errorCode': -7, 'errorMsg': '参数不合法！'}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())


if __name__ == '__main__':
    unittest.main()

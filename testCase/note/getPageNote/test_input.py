import unittest
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.yamlOperation import ReadYaml
from common.caseLogsMethod import info, step, class_case_log, func_case_log
from businessCommon.apiRe import ApiRe
from businessCommon.businessNote import BusinessNote


@class_case_log
class GetPageNoteInput(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    host = envConfig['host']
    path = apiConfig['getPageNote']['path']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    input = ReadYaml().api_yaml('checkInput.yml')
    userIdTestCase = input['checkInputString']
    userIdTestCase[3][0]["value"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    # print(userIdTestCase[3][0]["value"])

    startIndexTestCase = input['checkInputInter']

    # startIndexTestCase.pop(0)
    # print(startIndexTestCase.pop(0))

    def setUp(self) -> None:
        BusinessNote.clear_note(self.user_id, self.sid)

    @parameterized.expand(userIdTestCase)
    def testCase01_user_id(self, dic):
        """获取首页便签列表   userid验证"""
        note_ids = BusinessNote.multi_set_note(1, self.sid, self.user_id)
        start_index = 0
        rows = 0
        user_id = dic['value']
        print(user_id)
        url = self.url.format(userid=user_id, startindex=start_index, rows=rows)
        # print(url)
        step("STEP:获取首页便签列表")
        res = self.apiRe.note_get(url, self.sid)
        if dic['code'] == 404:
            self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
            expect = {
                'timestamp': str,
                'status': 404,
                'error': 'Not Found',
                'message': 'No message available',
                'path': '/v3/notesvr/user//home/startindex/0/rows/0/notes'
            }

            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())
        else:
            self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
            expect = {'errorCode': -7, 'errorMsg': str}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())

    @parameterized.expand(startIndexTestCase)
    def testCase02_start_index(self, dic):
        """获取首页便签列表   start_index验证"""

        note_ids = BusinessNote.multi_set_note(1, self.sid, self.user_id)
        start_index = dic['value']
        print(start_index)
        rows = 10

        url = self.url.format(userid=self.user_id, startindex=start_index, rows=rows)
        # print(url)
        step("STEP:获取首页便签列表")
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码错误')
        expect = {'errorCode': -7, 'errorMsg': str}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())

    @parameterized.expand(startIndexTestCase)
    def testCase03_rows(self, dic):
        """获取首页便签列表   rows验证"""
        note_ids = BusinessNote.multi_set_note(1, self.sid, self.user_id)
        start_index = 0
        rows = dic['value']
        url = self.url.format(userid=self.user_id, startindex=start_index, rows=rows)
        # print(url)
        step("STEP:获取首页便签列表")
        res = self.apiRe.note_get(url, self.sid)
        self.assertEqual(500, res.status_code, msg='状态码错误')
        expect = {'errorCode': -7, 'errorMsg': str}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())


if __name__ == '__main__':
    unittest.main()

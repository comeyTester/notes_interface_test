import unittest
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.yamlOperation import ReadYaml
from common.caseLogsMethod import info, step, class_case_log, func_case_log
from businessCommon.apiRe import ApiRe
from businessCommon.businessNote import BusinessNote
from copy import deepcopy


@class_case_log
class SetNoteInfoInput(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('testData.yml','setNoteInfo')
    host = envConfig['host']
    path = apiConfig['path']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    strTestCase = apiConfig['checkInputString']
    strTestCase[3][0]["value"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    # print(userIdTestCase[3][0]["value"])

    intTestCase = apiConfig['checkInputInter']

    base_body = {
        'noteId': 'note_id',
        'star': 0,
        'remindTime': 0,
        'remindType': 0
    }  # 缺少groupId

    # startIndexTestCase.pop(0)
    # print(startIndexTestCase.pop(0))
    # @unittest.skip
    @parameterized.expand(strTestCase)
    def testCase01_noteId(self, dic):
        """上传/更新便签主体   userid验证"""

        note_id = dic['value']
        print(note_id)
        body = deepcopy(self.base_body)
        body['noteId'] = note_id

        step("STEP:获取首页便签列表")
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
        if dic['code'] == 200:
            expect = {'responseTime':int, 'infoVersion': int, 'infoUpdateTime': int}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())
        else:
            expect = {'errorCode': int, 'errorMsg': str}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())

    # @unittest.skip
    @parameterized.expand(intTestCase)
    def testCase02_star(self, dic):
        """上传/更新便签主体   star验证"""

        star = dic['value']
        print(star)
        body = deepcopy(self.base_body)
        body['star'] = star

        step("STEP:获取首页便签列表")
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # self.assertEqual(500, res.status_code, msg='状态码错误')
        self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
        if dic['code'] == 200:
            expect = {'responseTime':int, 'infoVersion': int, 'infoUpdateTime': int}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())
        else:
            expect = {'errorCode': int, 'errorMsg': str}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())

    # @unittest.skip
    @parameterized.expand(strTestCase)
    def testCase02_star(self, dic):
        """上传/更新便签主体   groupId验证"""

        group_id = dic['value']
        print(group_id)
        body = deepcopy(self.base_body)
        body['groupId'] = group_id

        step("STEP:获取首页便签列表")
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # self.assertEqual(500, res.status_code, msg='状态码错误')
        self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
        if dic['code'] == 200:
            expect = {'responseTime':int, 'infoVersion': int, 'infoUpdateTime': int}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())
        else:
            expect = {'errorCode': int, 'errorMsg': str}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())


if __name__ == '__main__':
    unittest.main()

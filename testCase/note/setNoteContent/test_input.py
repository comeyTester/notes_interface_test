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
class SetNoteContentInput(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('testData.yml', 'setNoteContent')
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
        'noteId': "note_id",
        'title': 'test_title',
        'summary': 'test_summary',
        'body': 'test_body',
        'localContentVersion': "info_version",
        'BodyType': 0
    }

    @parameterized.expand(strTestCase)
    # @unittest.skip
    def testCase01_noteId(self, dic):
        """上传/更新便签内容   noteId验证"""

        note_id = dic['value']
        print(note_id)
        body = deepcopy(self.base_body)
        body['noteId'] = note_id

        step("STEP:获取首页便签列表")
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
        if dic['code'] == 200:
            expect = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())
        else:
            expect = {'errorCode': int, 'errorMsg': str}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())

    # @unittest.skip
    @parameterized.expand(strTestCase)
    # @unittest.skip
    def testCase02_title(self, dic):
        """上传/更新便签内容   title验证"""

        star = dic['value']
        print(star)
        body = deepcopy(self.base_body)
        body['star'] = star

        step("STEP:获取首页便签列表")
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # self.assertEqual(500, res.status_code, msg='状态码错误')
        self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
        if dic['code'] == 200:
            expect = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())
        else:
            expect = {'errorCode': int, 'errorMsg': str}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())

    @parameterized.expand(strTestCase)
    # @unittest.skip
    def testCase03_summary(self, dic):
        """上传/更新便签内容   summary验证"""

        group_id = dic['value']
        print(group_id)
        body = deepcopy(self.base_body)
        body['groupId'] = group_id

        step("STEP:获取首页便签列表")
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # self.assertEqual(500, res.status_code, msg='状态码错误')
        self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
        if dic['code'] == 200:
            expect = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())
        else:
            expect = {'errorCode': int, 'errorMsg': str}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())

    @parameterized.expand(strTestCase)
    # @unittest.skip
    def testCase04_body(self, dic):
        """上传/更新便签内容  body验证"""
        group_id = dic['value']
        print(group_id)
        body = deepcopy(self.base_body)
        body['groupId'] = group_id

        step("STEP:获取首页便签列表")
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # self.assertEqual(500, res.status_code, msg='状态码错误')
        self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
        if dic['code'] == 200:
            expect = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())
        else:
            expect = {'errorCode': int, 'errorMsg': str}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())

    @parameterized.expand(intTestCase)
    # @unittest.skip
    def testCase05_localContentVersion(self, dic):
        """上传/更新便签内容  localContentVersion验证"""
        group_id = dic['value']
        print(group_id)
        body = deepcopy(self.base_body)
        body['groupId'] = group_id

        step("STEP:获取首页便签列表")
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # self.assertEqual(500, res.status_code, msg='状态码错误')
        self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
        if dic['code'] == 200:
            expect = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())
        else:
            expect = {'errorCode': int, 'errorMsg': str}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())

    @parameterized.expand(intTestCase)
    # @unittest.skip
    def testCase06_BodyType(self, dic):
        """上传/更新便签内容 BodyType验证"""
        group_id = dic['value']
        print(group_id)
        body = deepcopy(self.base_body)
        body['groupId'] = group_id

        step("STEP:获取首页便签列表")
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        # self.assertEqual(500, res.status_code, msg='状态码错误')
        self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
        if dic['code'] == 200:
            expect = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())
        else:
            expect = {'errorCode': int, 'errorMsg': str}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())


if __name__ == '__main__':
    unittest.main()

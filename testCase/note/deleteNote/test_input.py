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
class DeleteNoteInput(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('testData.yml', 'deleteNote')
    host = envConfig['host']
    path = apiConfig['path']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    strTestCase = apiConfig['checkInputString']
    strTestCase[3][0]["value"] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"



    @parameterized.expand(strTestCase)
    # @unittest.skip
    def testCase01_noteId(self, dic):
        """删除便签 noteId-input校验"""
        step('STEP:新增一条便签内容')
        note_id = dic['value']
        body = {
            'noteId': note_id
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        if dic['code'] == 500:
            self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
            expect = {'errorCode': -7, 'errorMsg': int}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())

        else:
            self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
            expect = {'responseTime': int}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())







if __name__ == '__main__':
    unittest.main()

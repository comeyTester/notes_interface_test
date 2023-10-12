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
class GetNoteBodyInput(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('testData.yml', 'getNoteBody')
    host = envConfig['host']
    path = apiConfig['path']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    listTestCase = apiConfig['checkInputList']


    @parameterized.expand(listTestCase)
    # @unittest.skip
    def testCase01_noteIds(self, dir):
        """获取便签主体内容 主流程"""
        step('STEP:新增一条便签内容')
        note_id = BusinessNote.multi_set_note(1, self.sid, self.user_id)
        note_ids = dir['value']

        body = {
            'noteIds': note_ids
        }
        step("STEP:获取便签主体内容")
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        if dir['code'] == 500:
            self.assertEqual(dir['code'], res.status_code, msg='状态码错误')

            expect = {'errorCode': int, 'errorMsg':str}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())
        else:
            self.assertEqual(dir['code'], res.status_code, msg='状态码错误')
            expect = {'responseTime': int, 'noteBodies': list}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())



if __name__ == '__main__':
    unittest.main()

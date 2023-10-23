import unittest
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.yamlOperation import ReadYaml
from common.caseLogsMethod import info, step, class_case_log, func_case_log
from businessCommon.apiRe import ApiRe
from businessCommon.businessNote import BusinessNote


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
    BusinessNote = BusinessNote()
    base_body = {
        'noteId': "note_id",
        'title': 'test_title',
        'summary': 'test_summary',
        'body': 'test_body',
        'localContentVersion': "info_version",
        'BodyType': 0
    }

    def setUp(self) -> None:
        pass

    def testCase01_time_limit(self):
        """设置便签内容 时序限制   未生成便签主体，直接生成便签内容"""
        step("STEP:前置步骤：清空便签的数据")
        BusinessNote.clear_note(self.user_id, self.sid)
        step("STEP：请求设置便签内容")
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = self.base_body
        body["note_id"] = note_id
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        step("STEP：断言")
        self.assertEqual(500, res.status_code, msg='状态码错误')
        expect = {"errorCode": int, "errorMsg": str}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())



    def testCase02_operate_permission(self):
        """设置便签内容 操作权限验证"""


if __name__ == '__main__':
    unittest.main()

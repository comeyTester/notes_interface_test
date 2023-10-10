
import unittest
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.yamlOperation import ReadYaml
from common.caseLogsMethod import info, class_case_log, func_case_log
from businessCommon.apiRe import ApiRe


@class_case_log
class DeleteNoteLevel1(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    host = envConfig['host']
    path = apiConfig['deleteNote']['path']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()

    def testCase01_major(self):
        """删除便签 主流程"""
        info('STEP:获取便签主体版本')
        note_id = '1696489471551_noteId0'
        body = {
            'noteId': note_id
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码错误')
        expect = {'responseTime': int}
        info(f'expect body:{expect}')
        CheckTools().check_output(expect, res.json())

import unittest
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.yamlOperation import ReadYaml
from common.caseLogsMethod import info, class_case_log, func_case_log
from businessCommon.apiRe import ApiRe


@class_case_log
class GetNoteBodyLevel1(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('api.yml')
    host = envConfig['host']
    path = apiConfig['getNoteBody']['path']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()

    def testCase01_major(self):
        """获取便签主体内容 主流程"""
        info('STEP:获取便签主体版本')
        note_ids = ['1696489471551_noteId0']
        body = {
            'noteIds': note_ids
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码错误')
        expect = {'responseTime': int,
                  'noteBodies':[
                      {
                          'summary': str,
                          'noteId': str,
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


if __name__ == '__main__':
    unittest.main()

import unittest
import requests
import time
from common.checkCommon import CheckTools


class SetNoteInfo(unittest.TestCase):
    url = 'http://note-api.wps.cn' + '/v3/notesvr/set/noteinfo'

    headers = {
        'Content-Type': 'application/json',
        'X-user-key': '1084089582',
        'Cookie': 'wps_sid=V02S038CSTZXkRDG73zTQEt6IrBuqFM00a7cd34000409de4ee'
    }

    def testCase01_major(self):
        """上传/更新便签信息主体-主流程"""

        note_id = str(int(time.time() * 1000)) + '_test_noteId'

        body = {
            'noteId': note_id
        }

        res = requests.post(url=self.url, headers=self.headers, json=body)
        print(res.status_code)
        print(res.json())
        self.assertEqual(200, res.status_code, msg='状态码错误')
        expect = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        CheckTools().check_output(expect, res.json())
        # expect = {'responseTime': int, 'infoVersion': {'key': str}, 'infoUpdateTime': int}
        # actual = {'responseTime': 35, 'infoVersion': {'key': 'abc'}, 'infoUpdateTime': 1695794803625}
        # CheckTools().check_output(expect, actual)

    def testCase02_mast_input(self):
        """上传/更新便签信息主体 必填字段校验"""
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id

        }
        body.pop('noteId')

        res = requests.post(url=self.url, headers=self.headers, json=body)
        self.assertEqual(500, res.status_code, msg='状态码错误')
        expect = {'errorCode': int, 'errorMsg': str}
        CheckTools().check_output(expect, res.json())

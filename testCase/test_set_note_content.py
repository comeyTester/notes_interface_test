import unittest
import requests
import time
from common.checkCommon import CheckTools
from parameterized import parameterized


class SetNoteContent(unittest.TestCase):

    host = 'http://note-api.wps.cn'
    path = '/v3/notesvr/set/notecontent'
    url = host + path
    sid = 'V02S038CSTZXkRDG73zTQEt6IrBuqFM00a7cd34000409de4ee'
    user_id = '1084089582'



    must_key = ([{'key': 'noteId', 'code': 500}], [{'key': 'title', 'code': 200}], [{'key': 'summary', 'code': 200}],[{'key': 'body', 'code': 412}], [
        {'key': 'localContentVersion', 'code': 200}],[{'key': 'BodyType', 'code': 200}])

    def testcase01_major(self):
        """上传/更新便签内容 主流程"""

        headers = {
            'Content-Type': 'application/json',
            'X-user-key': self.user_id,
            'Cookie': f'wps_sid={self.sid}'
        }

        print('前置：获取便签主体版本')
        note_info_url = 'http://note-api.wps.cn' + '/v3/notesvr/set/noteinfo'
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id
        }
        note_info_res = requests.post(url=note_info_url, headers=headers, json=body)
        info_version = note_info_res.json()['infoVersion']

        title = str(int(time.time() * 1000)) + '_test_title'
        summary = str(int(time.time() * 1000)) + '_test_summary'
        body = str(int(time.time() * 1000)) + '_test_body'
        body = {
            'noteId': note_id,
            'title': title,
            'summary': summary,
            'body': body,
            'localContentVersion': info_version,
            'BodyType': 0
        }
        print('操作：新增便签内容')
        res = requests.post(url=self.url, headers=headers, json=body)
        self.assertEqual(200, res.status_code, msg='状态码错误')
        expect = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
        CheckTools().check_output(expect, res.json())
        # print(res.status_code)
        # print(res.json())

    @parameterized.expand(must_key)
    def testcase02_must_input(self, dic):
        """上传/更新便签内容 必填项校验"""
        print(f'必填项校验的字段{dic}')
        print('前置：获取便签主体版本')
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': self.user_id,
            'Cookie': f'wps_sid={self.sid}'
        }
        note_info_url = 'http://note-api.wps.cn' + '/v3/notesvr/set/noteinfo'
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id
        }
        note_info_res = requests.post(url=note_info_url, headers=headers, json=body)
        info_version = note_info_res.json()['infoVersion']

        title = str(int(time.time() * 1000)) + '_test_title'
        summary = str(int(time.time() * 1000)) + '_test_summary'
        body = str(int(time.time() * 1000)) + '_test_body'
        body = {
            'noteId': note_id,
            'title': title,
            'summary': summary,
            'body': body,
            'localContentVersion': info_version,
            'BodyType': 0
        }

        body.pop(dic['key'])
        print('操作：新增便签内容')
        res = requests.post(url=self.url, headers=headers, json=body)
        if dic['code'] == 200:
            self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
            expect = {'responseTime': int, 'contentVersion': int, 'contentUpdateTime': int}
            CheckTools().check_output(expect, res.json())
        else:
            self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
            expect = {'errorCode': int, 'errorMsg': str}
            CheckTools().check_output(expect, res.json())



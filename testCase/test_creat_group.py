import requests
import unittest
import time


class TestGroupClass(unittest.TestCase):
    # @unittest.skip
    def testCast_major(self):
        """新建分组的主流程"""
        URL = 'http://note-api.wps.cn' + '/v3/notesvr/set/notegroup'
        headers = {
            'Content-Type': 'application/json',
            'X-user-key': '1084089582',
            'Cookie': 'wps_sid=V02S038CSTZXkRDG73zTQEt6IrBuqFM00a7cd34000409de4ee'
        }

        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        group_name = str(int(time.time() * 1000)) + '_test_groupName'

        body = {
            'groupId': group_id,
            'groupName': group_name,
            'order': 0
        }

        res = requests.post(url=URL, headers=headers, json=body)
        # print(res.json().keys())


        assert res.status_code == 200
        assert 'responseTime' in res.json().keys()
        assert type(res.json()['responseTime']) == int
        assert 'updateTime' in res.json().keys()
        assert type(res.json()['updateTime']) == int
        assert len(res.json().keys()) == 2

        get_note_group_url = 'http://note-api.wps.cn' + '/v3/notesvr/get/notegroup'
        get_note_group_body = {}
        get_note_group_res = requests.post(url=get_note_group_url, headers=headers, json=get_note_group_body)
        # print(get_note_group_res.status_code)
        # print(get_note_group_res.json())

        group_ids = []
        group_names = []
        for item in get_note_group_res.json()['noteGroups']:
            group_id = item['groupId']
            group_name = item['groupName']
            group_ids.append(group_id)
            group_names.append(group_name)
        assert group_id in group_ids
        assert group_name in group_names

    def test_case02(self):
        """必填项校验"""
        print('testcase02')

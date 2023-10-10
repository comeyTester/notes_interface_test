import requests
import time

URL = 'http://note-api.wps.cn'+'/v3/notesvr/set/notegroup'
headers = {
    'Content-Type': 'application/json',
    'X-user-key': '1084089582',
    'Cookie': 'wps_sid=V02S038CSTZXkRDG73zTQEt6IrBuqFM00a7cd34000409de4ee'
}

groupId = str(int(time.time()*1000))+'_test_groupId'
groupName = str(int(time.time()*1000))+'_test_groupName'

body = {
    'groupId': groupId,
    'groupName': groupName,
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


get_note_group_url = 'http://note-api.wps.cn'+'/v3/notesvr/get/notegroup'
get_note_group_body ={}
get_note_group_res = requests.post(url=get_note_group_url, headers=headers, json=get_note_group_body)
# print(get_note_group_res.status_code)
# print(get_note_group_res.json())

groupIds = []
groupNames = []
for item in get_note_group_res.json()['noteGroups']:
    groupId = item['groupId']
    groupName = item['groupName']
    groupIds.append(groupId)
    groupNames.append(groupName)
assert groupId in groupIds
assert groupName in groupNames
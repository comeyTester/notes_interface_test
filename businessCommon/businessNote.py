"""
1、批量生成便签 形参定义 num、sid、user_id   return noteids # 新增便签主体 新增便签内容
2、清空用户便签数据
"""


import json
import time
from common.yamlOperation import ReadYaml
from businessCommon.apiRe import ApiRe


class BusinessNote:
    """
    便签相关的通用方法
    """

    # sid = envConfig['sid']
    # user_id = envConfig['user_id']

    @staticmethod
    def multi_set_note(num, sid, user_id):
        """
        批量生成便签
        1、涉及三个接口，设置便签主体，设置便签内容，查询便签列表
        2、通过便签列表获取 note_id
        :param num:
        :param sid:
        :param user_id:
        :return: note_ids
        """
        envconfig = ReadYaml().env_yaml()
        api_config = ReadYaml().api_yaml('api.yml')
        host = envconfig['host']
        api_re = ApiRe()
        note_ids = []
        for i in range(num):
            note_info_path = api_config["setNoteInfo"]["path"]
            note_info_url = host + note_info_path
            note_id = str(int(time.time() * 1000)) + '_test_noteId'
            note_ids.append(note_id)
            body = {
                'noteId': note_id
            }
            note_info_res = api_re.note_post(note_info_url, user_id, sid, body)
            # print(note_info_res.json())
            info_version = note_info_res.json()["infoVersion"]
            set_note_content_body = {
                'noteId': note_id,
                'title': 'test_title',
                'summary': 'test_summary',
                'body': 'test_body',
                'localContentVersion': info_version,
                'BodyType': 0
            }
            note_content_path = api_config["setNoteContent"]["path"]
            note_content_url = host + note_content_path
            set_note_content_res = api_re.note_post(note_content_url, user_id, sid, set_note_content_body)
            # print(set_note_content_res.json())
        return note_ids

    @staticmethod
    def clear_note(user_id, sid):
        """
        清空用户便签数据
        :param user_id:
        :param sid:
        :return: 0
        """
        envconfig = ReadYaml().env_yaml()
        api_config = ReadYaml().api_yaml('api.yml')
        host = envconfig['host']
        api_re = ApiRe()
        get_page_note_path = api_config["getPageNote"]["path"]
        get_page_note_url = host + get_page_note_path
        start_index = 0
        rows = 0
        url = get_page_note_url.format(userid=user_id, startindex=start_index, rows=rows)
        res = api_re.note_get(url, sid)
        assert res.status_code == 200, "状态码错误"
        # print(res.json())
        note_ids = []
        for i in res.json()["webNotes"]:
            # print(i["noteId"])
            note_id = i["noteId"]
            note_ids.append(note_id)
        # print(note_ids)

        delete_note_path = api_config["deleteNote"]["path"]
        delete_note_url = host + delete_note_path
        for i in note_ids:
            note_id = i
            body = {
                'noteId': note_id
            }
            delete_note_res = api_re.note_post(delete_note_url, user_id, sid, body)
            assert delete_note_res.status_code == 200, "状态码错误"
        path = api_config['cleanRecycleBin']['path']
        url = host + path
        body = {
            'noteIds': ['-1']
        }
        res = api_re.note_post(url, user_id, sid, body)
        assert res.status_code == 200, "状态码错误"
        return 0


if __name__ == '__main__':
    envConfig = ReadYaml().env_yaml()
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    a = BusinessNote()

    print(a.multi_set_note(3,sid,user_id))
    # print(a.clear_note(user_id, sid))

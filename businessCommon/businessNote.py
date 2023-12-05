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
    def clear_note(userid, sid):
        """
        清空用户便签数据
        :param userid:
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
        url = get_page_note_url.format(userid=userid, startindex=start_index, rows=rows)
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
            delete_note_res = api_re.note_post(delete_note_url, userid, sid, body)
            assert delete_note_res.status_code == 200, "状态码错误"
        path = api_config['cleanRecycleBin']['path']
        url = host + path
        body = {
            'noteIds': ['-1']
        }
        res = api_re.note_post(url, userid, sid, body)
        assert res.status_code == 200, "状态码错误"
        return 0

    @staticmethod
    def get_note_ids(userid, sid):
        """
        获取便签列表下的便签ID
        :return:
        """
        envconfig = ReadYaml().env_yaml()
        api_config = ReadYaml().api_yaml('api.yml')
        host = envconfig['host']
        get_page_note_path = api_config["getPageNote"]["path"]
        get_page_note_url = host + get_page_note_path
        api_re = ApiRe()
        start_index = 0
        rows = 0
        url = get_page_note_url.format(userid=userid, startindex=start_index, rows=rows)
        note_ids = []
        res = api_re.note_get(url, sid)
        for i in res.json()['webNotes']:
            note_id = i['noteId']
            note_ids.append(note_id)
        print(res.json())
        return note_ids

    @staticmethod
    def get_group_ids(userid, sid):
        """
    获取全部的groupID
        :param userid:
        :param sid:
        :return:
        """
        envconfig = ReadYaml().env_yaml()
        api_config = ReadYaml().api_yaml('api.yml')
        host = envconfig['host']
        api_re = ApiRe()
        path = api_config['getNoteGroup']['path']
        url = host + path
        body = {}
        res = api_re.note_post(url, userid, sid, body)
        group_ids = []
        for i in res.json()['noteGroups']:
            group_id = i['groupId']
            group_ids.append(group_id)
        print(res.json())
        return group_ids

    @staticmethod
    def clear_group(userid, sid):
        """
        清空组ID
        :param userid:
        :param sid:
        :return:
        """
        envconfig = ReadYaml().env_yaml()
        api_config = ReadYaml().api_yaml('api.yml')
        host = envconfig['host']
        api_re = ApiRe()
        group_ids = BusinessNote().get_group_ids(userid, sid)
        path = api_config['deleteNoteGroup']['path']
        url = host + path
        body = {
            'groupId': ""
        }
        for i in group_ids:
            body['groupId'] = i
            res = api_re.note_post(url, userid, sid, body)
        return 0

    @staticmethod
    def multi_set_note_group(num, user_id, sid):
        """
        批量生成便签组ID
        :param num:
        :param user_id:
        :param sid:
        :return:
        """
        envconfig = ReadYaml().env_yaml()
        api_config = ReadYaml().api_yaml('api.yml')
        host = envconfig['host']
        api_re = ApiRe()
        path = api_config['setNoteGroup']['path']
        url = host + path
        group_ids = []
        for i in range(num):
            group_id = str(int(time.time() * 1000)) + '_test_groupId'
            group_ids.append(group_id)
            body = {
                'groupId': group_id,
                'groupName': 'test_groupName',
                'order': 0
            }
            res = api_re.note_post(url, user_id, sid, body)
        return group_ids

    @staticmethod
    def set_note_has_group_id(group_id, user_id, sid):
        """新增一条便签，绑定指定的groupID"""
        envconfig = ReadYaml().env_yaml()
        api_config = ReadYaml().api_yaml('api.yml')
        host = envconfig['host']
        api_re = ApiRe()
        note_info_path = api_config["setNoteInfo"]["path"]
        note_info_url = host + note_info_path
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        body = {
            'noteId': note_id,
            'groupId': group_id
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
        return note_id

    @staticmethod
    def delete_note(note_id, user_id, sid):
        """
        删除指定的便签数据
        :param note_id:
        :param user_id:
        :param sid:
        :return:
        """
        envconfig = ReadYaml().env_yaml()
        api_config = ReadYaml().api_yaml('api.yml')
        host = envconfig['host']
        api_re = ApiRe()
        delete_note_path = api_config["deleteNote"]["path"]
        delete_note_url = host + delete_note_path
        body = {
            'noteId': note_id
        }
        delete_note_res = api_re.note_post(delete_note_url, user_id, sid, body)
        return note_id

    @staticmethod
    def get_recycle_bin_list(user_id, sid):
        envconfig = ReadYaml().env_yaml()
        api_config = ReadYaml().api_yaml('api.yml')
        host = envconfig['host']
        api_re = ApiRe()
        path = api_config["getRecycleBinList"]["path"]
        start_index = 0
        rows = 0
        path = path.format(userid=user_id, startindex=start_index, rows=rows)
        url = host + path
        res = api_re.note_get(url, sid)
        note_ids = []
        for i in res.json()['webNotes']:
            note_id = i['noteId']
            note_ids.append(note_id)
        return note_ids

    @staticmethod
    def get_note_info(note_id, user_id, sid):
        """
        获取的单个noteid的便签信息
        :param note_id:
        :param user_id:
        :param sid:
        :return:
        """
        envconfig = ReadYaml().env_yaml()
        api_config = ReadYaml().api_yaml('api.yml')
        host = envconfig['host']
        get_page_note_path = api_config["getPageNote"]["path"]
        get_page_note_url = host + get_page_note_path
        api_re = ApiRe()
        start_index = 0
        rows = 0
        url = get_page_note_url.format(userid=user_id, startindex=start_index, rows=rows)
        note_info = []
        res = api_re.note_get(url, sid)
        for i in res.json()['webNotes']:
            if i['noteId'] == note_id:
                note_info.append(i)
                # print(i)
        return note_info


if __name__ == '__main__':
    envConfig = ReadYaml().env_yaml()
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    a = BusinessNote()

    # print(a.multi_set_note(1, sid, user_id))
    # print(a.clear_note(user_id, sid))
    # print(a.get_note_ids(user_id, sid))
    # print(a.get_group_ids(user_id, sid))
    # print(a.clear_group(user_id, sid))
    # note_id = "'1697082697940_test_noteId'"
    # print(a.delete_note(note_id, user_id, sid))
    # print(a.get_recycle_bin_list(user_id, sid))
    note_ids = a.multi_set_note(1, sid, user_id)
    note_id = note_ids[0]
    print(a.get_note_info(note_id,user_id,sid))
    b = a.get_note_info(note_id,user_id,sid)
    print(b[0]['star'])

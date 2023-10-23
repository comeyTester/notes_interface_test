import unittest
import time
from common.checkCommon import CheckTools
from parameterized import parameterized
from common.yamlOperation import ReadYaml
from common.caseLogsMethod import info, step, class_case_log, func_case_log
from businessCommon.apiRe import ApiRe
from businessCommon.businessNote import BusinessNote


@class_case_log
class SetNoteInfoInput(unittest.TestCase):
    envConfig = ReadYaml().env_yaml()
    apiConfig = ReadYaml().api_yaml('testData.yml', 'setNoteInfo')
    host = envConfig['host']
    path = apiConfig['path']
    url = host + path
    sid = envConfig['sid']
    user_id = envConfig['user_id']
    apiRe = ApiRe()
    BusinessNote = BusinessNote()
    star_enum = apiConfig["star_enum"]
    print(star_enum)

    def setUp(self) -> None:
        pass

    def testCase01_group_id_limit(self):
        """设置便签主体 groupId   约束条件-便签ID不存在，是否可以绑定成功"""
        step("STEP:前置步骤：清空用户组ID的数据")
        # BusinessNote.clear_group(self.user_id, self.sid)  # groupId不能被删除BUG
        step("STEP:确定groupId是不存在的")
        group_ids = BusinessNote.get_group_ids(self.user_id, self.sid)
        group_id = str(int(time.time() * 1000)) + '_test_groupId'
        if group_id not in group_ids:
            step("STEP请求便签主体，便签ID不存在")
            note_id = str(int(time.time() * 1000)) + '_test_noteId'
            body = {
                'noteId': note_id,
                'groupId': group_id
            }
            res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
            step("STEP：断言")
            self.assertEqual(500, res.status_code, msg='状态码错误')
            expect = {"errorCode": -7, "errorMessage": ""}
            info(f'expect body:{expect}')
            CheckTools().check_output(expect, res.json())
        else:
            print("groupId生成失败")

    def testCase02_note_id_limit(self):
        """设置便签主体 noteId重复，进入便签主体更新流程"""
        # 生成一个便签主体 更新便签主体内容
        step("STEP:新增一个便签主体")
        note_ids = BusinessNote.multi_set_note(1, self.sid, self.user_id)
        note_id = note_ids[0]
        step("STEP:noteId重复，进入便签主体更新流程")
        body = {
            'noteId': note_id,
            'star': 1
        }
        step("STEP:更新便签主体内容")
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(200, res.status_code, msg='状态码错误')
        expect = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        CheckTools().check_output(expect, res.json())
        step("STEP:验证更新的主体内容写入成功")
        note_info = BusinessNote.get_note_info(note_id, self.user_id, self.sid)
        # print(note_info)
        self.assertEqual(1, note_info[0]['star'], msg='验证更新的内容失败')

    @parameterized.expand(star_enum)
    def testCase03_star_enum(self, dic):
        """设置便签主体  star枚举值验证-枚举值1是标星，0是不标星，默认值为0"""
        step("STEP:新增一个便签主体")
        note_id = str(int(time.time() * 1000)) + '_test_noteId'
        star = dic['value']
        body = {
            'noteId': note_id,
            'star': star
        }
        res = self.apiRe.note_post(self.url, self.user_id, self.sid, body)
        self.assertEqual(dic['code'], res.status_code, msg='状态码错误')
        expect = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
        CheckTools().check_output(expect, res.json())

    def testCase04_operate_permission(self):
        """设置便签主体 操作权限验证"""


if __name__ == '__main__':
    unittest.main()

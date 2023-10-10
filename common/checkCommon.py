import unittest


class CheckTools(unittest.TestCase):
    def check_output(self, expect, actual):
        """
        接口返回体与文档对齐
        校验点：
        1、返回的字段是否和文档一致
        2、返回的字段的类型是否一致
        3、没有多余的字段出现
        4、如果需要精确到值的校验，直接传递值即可
        :param expect:('responseTime': int, 'infoVersion': int, 'infoUpdateTime': int)
        :param actual:response.json()
        :return: None
        """
        self.assertEqual(len(expect.keys()), len(actual.keys()), msg='字段长度不匹配')  # 验证没有多余的字段出现
        for k, v in expect.items():
            if type(v) == dict:  # 遇到嵌套的字典，进行递归
                self.check_output(expect[k], actual[k])
            elif type(v) == list:
                self.assertEqual(len(v), len(actual[k]))
                for item in range(len(expect[k])):
                    if type(expect[k][item]) == dict:
                        self.check_output(expect[k][item], actual[k][item])
                    else:
                        if type(expect[k][item]) == type:
                            self.assertEqual(expect[k][item], type(actual[k][item]), msg=f'{k} 字段类型不一致')  # 校验类型
                        else:
                            self.assertEqual(type(expect[k][item]), type(actual[k][item]),
                                             msg=f'{k} 字段类型不一致')  # 校验类型
                            self.assertEqual(expect[k][item], actual[k][item], msg=f'{k} 字段值不一致')  # 校验类型
            else:
                self.assertIn(k, actual.keys(), msg=f'{k}字段不存在')  # 验证返回字段和文档的一致
                if type(v) == type:
                    self.assertEqual(v, type(actual[k]), msg=f'{k}字段类型不一致')  # 验证返回字段的类型和文档一致
                else:
                    self.assertEqual(type(v), type(actual[k]), msg=f'{k} 字段类型不一致')  # 校验类型
                    self.assertEqual(v, actual[k], msg=f'{k} 字段值不一致')





if  __name__ == '__main__':
    expect = {'responseTime': int, 'infoVersion': int, 'infoUpdateTime': int}
    actual = {'responseTime': 35, 'infoVersion': 1, 'infoUpdateTime': 1695794803625}
    CheckTools().check_output(expect, actual)














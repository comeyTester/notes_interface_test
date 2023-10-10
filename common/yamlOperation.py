import yaml
from common.getProjectPath import *

'''yaml文件数据结构
对象：键值对的集合(简称："映射或字典")
键值对用冒号:结构来表示，冒号与值之间需用空格分隔
数组: 一组按序排列的值(简称"序列或表")
数组前加有-符号，符号与值之间需用空格分隔
纯量(scalars): 单个的、不可再分的值(如：字符串、bool值、整数、浮点数、时间、日期、null等) None值可用null 或 ~表示
'''

'''
yaml.load(f, Loader=yaml.FullLoader)  
yaml.load_all(f, Loader=yaml.FullLoader)  #---分隔两个文件，使用方法读取两个yaml文件的数据，读取多个文档
yaml.dump()  # 使用读dump()方法写入数据。第一个参数是数据，第二个参数是文件对象
yaml.dump(data, sort_keys=TRUE) #可以使用dump's sort_keys 参数对键进行排序
'''


class ReadYaml:
    """读取配置数据"""

    @staticmethod
    def get_env():
        with open(os.path.join(CONF_DIR, 'env.yml'), 'r', encoding='utf-8') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            return data['env']

    @staticmethod
    def env_yaml():
        env = ReadYaml().get_env()
        if env == 'Online':
            with open(os.path.join(ONLINE_CONF_DIR, 'config.yml'), 'r', encoding='utf-8') as f:
                return yaml.load(f, Loader=yaml.FullLoader)
        else:
            with open(os.path.join(OFFLINE_CONF_DIR, 'config.yml'), 'r', encoding='utf-8') as f:
                return yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def api_yaml(filename):
        with open(os.path.join(DATA_DIR, filename), 'r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)


if __name__ == '__main__':
    s = ReadYaml().api_yaml('checkInput.yml')
    print(s)
    # print(type(s['host']))

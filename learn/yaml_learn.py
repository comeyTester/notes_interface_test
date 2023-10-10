import yaml
import os
from common.getProjectPath import *

'''
yaml的语法规则
区分大小写
使用缩进表示层级关系
使用空格缩进，而非Tab键缩进
缩进的空格数目不固定，只需要相同层级的元素左侧对齐
文件中的字符串不需要引号标注，但若字符串中包含有特殊字符则需用引号标注
注释标识为 #
yaml文件数据结构
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
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
print(f'{BASE_DIR}\TestData\\test.yml')

with open(f'{BASE_DIR}\TestData\\test.yml', encoding='utf-8') as f:
    data = yaml.load_all(f, Loader=yaml.FullLoader)
    for i in data:
        print(i)

users = [{'name': 'John Doe', 'occupation': 'gardener'},
         {'name': 'Lucy Black', 'occupation': 'teacher'}]

with open(f'{BASE_DIR}\TestData\\test.yml', 'a') as f:
    data = yaml.dump(users, f)

with open(os.path.join(DATA_DIR, 'checkInput.yml'), 'a') as f:
    data1 = yaml.load(f, Loader=yaml.FullLoader)
    for i in data1:
        print(i)

from datetime import datetime
import inspect
import os
from colorama import Fore
from common.getProjectPath import *
import time
import functools


def info(text):
    current_time = datetime.now()
    formatted_time = current_time.strftime('%H:%M:S.%f')[:-3]  # 获取当前时间，精确到毫秒
    stack = inspect.stack()
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"
    text = f"[INFO]{code_path}-{formatted_time} >> {text} \n"
    print(Fore.LIGHTGREEN_EX + text.strip())
    str_time = current_time.strftime("%Y%m%d")
    log_name = "{}_info.log".format(str_time)
    with open(os.path.join(LOG_DIR,log_name), mode="a", encoding="utf-8") as f:
        f.write(text)


def error(text):
    current_time = datetime.now()
    formatted_time = current_time.strftime('%H:%M:%S.%f')[:-3]
    stack = inspect.stack()  # 获取方法执行的代码路径
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"
    text = f"[ERROR]{code_path}-{formatted_time} >> {text} \n"
    print(Fore.LIGHTRED_EX + text.strip())
    str_time = current_time.strftime("%Y%m%d")
    log_name = "{}_error.log".format(str_time)
    with open(os.path.join(LOG_DIR,log_name), mode="a", encoding="utf-8") as f:
        f.write(text)


def step(text):
    current_time = datetime.now()
    formatted_time = current_time.strftime('%H:%M:%S.%f')[:-3]
    stack = inspect.stack()  # 获取方法执行的代码路径
    code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"
    text = f"[INFO]{code_path}-{formatted_time} >> {text} \n"
    print(Fore.LIGHTBLUE_EX + text.strip())
    str_time = current_time.strftime("%Y%m%d")
    log_name = "{}_info.log".format(str_time)
    with open(os.path.join(LOG_DIR,log_name), mode="a", encoding="utf-8") as f:
        f.write(text)

def func_case_log(func):
    @functools.wraps(func)  # 不影响原有变量
    def inner(*args, **kwargs):
        print("")
        info(Fore.LIGHTBLUE_EX + "--------------------CASE START---------------------------")
        class_name = args[0].__class__.__name__  # 获取类名
        method_name = func.__name__  # 获取方法名
        docstring = inspect.getdoc(func)  # 获取方法注释
        info(f"Class Name: {class_name}")
        info(f"Method Name: {method_name}")
        info(f"Test Description: {docstring}")
        return func(*args, **kwargs)
    return inner


def class_case_log(cls):
    """用例的日志装饰器类级别"""
    for name, method in inspect.getmembers(cls, inspect.isfunction):
        if name.startswith('testCase'):
            setattr(cls, name, func_case_log(method))
    return cls


if __name__ == '__main__':
    info("abc")
    info("12345")
    error("1223")
    step("ddddddd")

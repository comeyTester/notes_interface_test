"""
Inspect模块是Python的标准库之一，它提供了一些有用的函数来获取正在运行的Python代码的信息。以下是Inspect模块的一些主要功能：

1、获取代码执行路径stack = inspect.stack()  code_path = f"{os.path.basename(stack[1].filename)}:{stack[1].lineno}"
2、获取类名，方法名，方法注释 inspect.getdoc(func)
3、获取类下面的方法列表 inspect.getmembers
"""

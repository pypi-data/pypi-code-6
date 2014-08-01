#从Python发布工具导入“setup”函数
from distutils.core import setup
#以下这些是setup函数的参数名
setup(
    name = 'wtest',    #模块名称
    version = '1.3.0',  #模块版本编号
    py_modules = ['wtest'],    #将模块的元数据与setup函数的参数关联
    #以下为模块作者的信息
    author = 'Wen Jacky',
    author_email = 'gn2018@163.com',
    url = 'http://www.nx96138.com',
    description = '这是我写的第一个python模块',
    )

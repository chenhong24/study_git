"""
json模块
loads:将字符串中的json数据转化为对应的python类型数据
dumps:将python数据转化为json数据，放在一个字符串里面

闭包函数：
函数中嵌套一个函数
外层函数返回的是内层函数的函数名
内层函数对外部作用域有非全局变量的引用（不能引用全局变量）

装饰器的作用：在不修改原功能代码的基础上，给代码拓展新的功能

可迭代对象（iterable）：只要通过for循环进行遍历的都叫可迭代对象

迭代器：能够使用next方法取值
所有可迭代对象都可以使用内置函数iter()转换为迭代器
生成器（generator）：生成器是一种特殊的迭代器
生成器比迭代器多了几个方法：
send():和生成内部进行数据交互

生成器的定义
1、生成器表达式
2、生成器函数
只要函数中定义yield这个关键字，那么这个函数就不再是一个普通的函数了，而是一个生成器函数
生成器函数在调用的时候，会自动返回一个生成器
深浅复制：只在数据嵌套的情况下讨论


"""

# def func(fu):
#     def wrapper():
#         print("开始执行")
#         fu()
#         print("执行结束")
#
#     return wrapper()
#
#
# @func
# def add():  # add = func(add)
#     a = 100
#     b = 200
#     print("a+b", a + b)
#
#
# add()
# li = [11, 22, 33]
# li2 = iter(li)
# print(next(li2))
# a = ["h", "e", "l", "l", "o"]
# b = "".join(a)
# print(b)
#
# with open("data.log", "r") as f:
#     list = f.readlines()
#     for i in range(0, len(list)):
#         list[i] = list[i].strip("\n")
#
# print(list)
# listc = list[1:]
# print(listc)
# listb = " ".join(listc)
#
# print(listb)
# print(len(listb))
# print(type(listb))

a = []
with open("data.log", "r", encoding="utf-8") as f:
    for line in f.readlines():
        a.append(line.strip())
    print(a)
keys = []
values = []
for key in a[0]:
    print(key)
# for value in enumerate(a):
#     values.append(value)
# result = dict(zip(keys, values))
# print(result)

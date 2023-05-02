#常见元组操作：
empty_tuple = ()
print("空元组",empty_tuple)

onetuple = "test",
print("元组只有一个数据值时需要跟着一个逗号", onetuple)


marx_tuple = ('Groucho', 'Chico', 'Harpo')
print(marx_tuple)

# 元组的解包；
a,b,c = marx_tuple
print(a)
print(b)
print(c)

"""
元组的特点和优势：
• 元组占用的空间较小
• 你不会意外修改元组的值
• 可以将元组用作字典的键(详见 3.4 节)
• 命名元组(详见第 6 章“命名元组”小节)可以作为对象的替代
• 函数的参数是以元组形式传递的(详见 4.7 节)
"""
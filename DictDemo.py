"""字典的操作"""
empty_dict= {}
print("空字典：", empty_dict)
#key 修改字典的值,其中字典的key是不可重复的

dict1 = {
'Chapman': 'Graham',
'Cleese': 'John',
'Idle': 'Eric',
'Jones': 'Terry',
'Palin': 'Michael',
}
dict1["Gillal"] = "Gerry"
print(dict1)

# 使用update合并字典的值
others = { 'Marx': 'Groucho', 'Howard': 'Moe',
'Palin': 'Michaels',}
dict1.update(others)
print(dict1)


# clear() 删除所以元素

# 使用in 判断元素是否存在

# [key] 获取到单个字典元素，keys获取到所有字典的键
print(dict1.keys())
# 通过list可以对dict_keys转换为列表类型
print(list(dict1.keys()))

# 获取到所有的值：values
print("获取到字典所有的值：", dict1.values())
print("获取到字典所有的值并转为列表：", list(dict1.values()))

#  获取到所有的键值对 items
print("获取到所有键值对：", dict1.items())


for key, value in dict1.items():
    print("字典的key:", key)
    print("字典的value:", value)

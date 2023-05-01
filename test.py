tinydict = {'Name': 'Runoob', 'Age': 7, 'Class': 'First', "data":{'Name': 'Runoob', 'Age': 7, 'Class': 'First'}}

for key, value in tinydict.items():
    print("获取键",key)
    print("获取值",value)


for key in tinydict.keys():
    print(key)


for value in tinydict.values():
    print(value)

print(id(tinydict))
tinydict.copy()
print(id(tinydict))
print(id(tinydict["data"]))


# 字典不同创建方式
seq = {"name", "age", "sex"}
dict1 = dict.fromkeys(seq, 111)
print(dict1)

# 字典有两个获取值的方法：1.get() 2.dict[key]
# get() 键不在字典时，返回默认值None
# 2.dict[key] 键不在字典时，会报错；
print("获取指定的值", dict1.get("name"))


tinydict2 = {'Sex': 'female' }
tinydict.update(tinydict2)
print(tinydict)
print(tinydict.clear())
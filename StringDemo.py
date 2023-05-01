# str可以类型转换
num1 = 1100
num2 = str(num1)
print(num2)
print(type(num2))
"""
分片操作(slice)可以从一个字符串中抽取子字符串(字符串的一部分)。我们使用一对方 括号、起始偏移量 start、终止偏移量 end 以及可选的步长 step 来定义一个分片。其中一 些可以省略。分片得到的子串包含从 start 开始到 end 之前的全部字符。
• [:] 提取从开头到结尾的整个字符串
• [start:] 从 start 提取到结尾
• [:end] 从开头提取到 end - 1
• [start:end] 从 start 提取到 end - 1
• [start:end:step] 从 start 提取到 end - 1，每 step 个字符提取一个
"""
print(num2[::-1])
print("获取长度len方法", len(num2))
todos = 'get gloves,get mask,give cat vitamins,call ambulance'
print(todos.split()) # 空格分割
print(todos.split(',')) # ，分割

# 指定分割次数
print("+++++++++")
resulttodos = todos.split(",",1)
print(resulttodos)
list = ['apple', 'banana', 'orange']
result = ''.join(list)
print(result)  # 'applebananaorange'
result = "_".join(list)
print(result)
dict = {'a': 'apple', 'b': 'banana', 'o': 'orange'}
result1 = "-".join(dict.keys())
result2 = "-.".join(dict.values())
print(result1)
print(result2)

def DealStringData(StringData):
    if len(StringData.split()) > 1:
        data1 = StringData.split()
        if "," in data1:
            data1 = data1.split(",")
    elif "," in StringData:
        data1 = StringData.split(",")
    else:
        data1 = StringData
    return data1


StringData = "apple,banana,orange"
print(DealStringData(StringData))

# 列表的操作

datalist = DealStringData(StringData)
datalist.append("dadad")
print("尾部添加数据", datalist)

# 列表的合并
others = ['Gummo', 'Karl']
datalist += others
print(datalist)

# insert操作，可以将元素插入到列表的任意位置，超出指定索引就会加入到尾部
datalist.insert(2, "12113")
print(datalist)
# del datalist[-1]
# print(datalist)
# 使用remove删除具有制定值的元素
print(datalist.remove("apple"))

#pop()或pop(-1)默认是删除列表尾部元素，pop(0)则返回列表的尾部元素

# index()查询特定值的元素位置
# count() 查询特定值出现的次数
#
# 列表的排序
# 升序排序
list1 = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
list1.sort()
print(list1)  # [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]

# 降序排序
list2 = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
list2.sort(reverse=True)
print(list2)  # [9, 6, 5, 5, 5, 4, 3, 3, 2, 1, 1]

# 与sort不同的是sorted函数对列表进行排序时返回一个新的列表，不会修改原有列表
# 升序排序
list1 = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
sorted_list1 = sorted(list1)
print(sorted_list1)  # [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]

# 降序排序
list2 = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
sorted_list2 = sorted(list2, reverse=True)
print(sorted_list2)  # [9, 6, 5, 5, 5, 4, 3, 3, 2, 1, 1]

# 按照元素的绝对值进行排序
list1 = [3, -1, 4, -1, 5, 9, 2, 6, 5, 3, 5]
sorted_list1 = sorted(list1, key=abs)
print(sorted_list1)  # [-1, -1, 2, 3, 3, 4, 5, 5, 5, 6, 9]

# 按照字母表顺序进行排序
list2 = ['apple', 'banana', 'Orange', 'cherry']
sorted_list2 = sorted(list2, key=str.lower)
print(sorted_list2)  # ['apple', 'banana', 'cherry', 'Orange']
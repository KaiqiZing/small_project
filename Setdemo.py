"""集合的使用"""

emptyset = set()
print("创建一个空集合：", emptyset)

even_numbers = {0, 2, 4, 6, 8}
print("集合特点是键是无序：", even_numbers)


# 列表创建集合
list1 = ['Dasher', 'Dancer', 'Prancer', 'Mason-Dixon']
print(set(list1))
# 再试试元组:
tuple1 = ('Ummagumma', 'Echoes', 'Atom Heart Mother')
print(set(tuple1))
# 当字典作为参数传入 set() 函数时，只有键会被使用:
dict1 = {'apple': 'red', 'orange': 'orange', 'cherry': 'red'}
print(set(dict1))

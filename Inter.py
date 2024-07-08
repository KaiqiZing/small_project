
class TestInter:

    def __init__(self, arry_list):
        self.arry_list = arry_list
        self.index = 0

    def __iter__(self):
        return self
    def __next__(self):
        if self.index < len(self.arry_list):
            value = self.arry_list[self.index]
            self.index += 1
            return value
        else:
            raise StopIteration


test = TestInter([1,3,4,5])
for i in test:
    print(i)


def check(fn):
    def inner():
        print("请登录。。。。。")
        fn()
    return inner

@check  #把内层函数的引用地址由check指向inner，转换成comment指向inner
def comment():
    print("发表评论")

comment()




zip_number = [1,2,3]
zip_string = ['one', "two","three", "four"]
result = zip(zip_number, zip_string)
print(set(result))
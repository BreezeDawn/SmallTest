from pymongo import MongoClient


class MongoStudy:
    def __init__(self):
        # 1.导入pymongo并选择要操作的集合 数据库和集合乜有会自动创建
        self.client = MongoClient(host='127.0.0.1', port=27017)
        self.col = self.client['maimai']['girls']

    def insert_one_test(self):
        # 2.插入单条数据
        ret = self.col.insert_one({"name": "test10010", "age": 33})
        print(ret)

    def insert_many_test(self):
        # 3.插入多条数据,insert_many接收一个列表，列表中为所有需要插入的字典
        item_list = [{"name": "test1000{}".format(i)} for i in range(10)]
        t = self.col.insert_many(item_list)
        print(t)

    def find_one_test(self):
        # 4.find_one查找并且返回一个结果,接收一个字典形式的条件
        t = self.col.find_one({"name": "test10005"})
        print(t)

    def find_test(self):
        # 5.find返回所有满足条件的结果，如果条件为空，则返回数据库的所有
        # 结果是一个Cursor游标对象，是一个可迭代对象，可以类似读文件的指针，但是只能够进行一次读取
        t = self.col.find({"name": "test10005"})
        for i in t:
            print(i)
        for i in t:  # 此时t中没有内容
            print(i)

    def update_one(self):
        # 6.update_one更新一条数据
        self.col.update_one({"name": "test10005"}, {"$set": {"name": "new_test10005"}})

    def update_many(self):
        # 7.update_many更新全部数据
        self.col.update_many({"name": "test10005"}, {"$set": {"name": "new_test10005"}})

    def delete_one(self):
        # 8.delete_one删除一条数据
        print(self.col.find_one({"name": "test10010"}))
        self.col.delete_one({"name": "test10010"})
        print(self.col.find_one({"name": "test10010"}))

    def delete_many(self):
        # 9.delete_may删除所有满足条件的数据
        self.col.delete_many({"name": "test10010"})

import pymysql
import datetime

#符合数据库格式的词典
class sql_dict():
    def __init__(self, time, v1, v2):
        self.time = time
        self.v1 = v1
        self.v2 = v2

#数据库操作类
class mysql:
    #连接数据库
    def db_connect(self):
        self.db = pymysql.connect(
            host="localhost", #连接主机
            port=3306, #端口
            user="wrq_bs", #用户名
            passwd="JJ7MPLK2htmwABxH", #密码
            db="wrq_bs" #库名
        )
        self.cursor = self.db.cursor()

    #数据库的基本提交指令
    def common_commit(self, sql, args):
        self.db_connect()
        try:
            self.cursor.execute(sql, args)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)
        finally:
            self.db.close()

    #数据库的基本搜索指令
    def common_search(self, sql, *args):
        self.db_connect()
        results = []
        try:
            if args:
                self.cursor.execute(sql, args[0])
            else:
                self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            self.db.close()
        return results

    #插入新数据
    def insert_data(self, data):
        sql = "INSERT INTO `wrq_bs`.`data` (`time`, `voltage1`, `voltage2`) \
            VALUES (CURRENT_TIMESTAMP, '%(v1)s', '%(v2)s')"
        args = (data)
        self.common_commit(sql, args)

    #查找某个小时的数据
    def search_by_hour(self, datetime):
        list = []
        sql = "SELECT * FROM `data` WHERE DATE(`time`) = DATE(%s) AND HOUR(`time`) = HOUR(%s)"
        args = (datetime, datetime)
        results = self.common_search(sql, args)
        for item in results:
            list.append(sql_dict(item[0].strftime("%Y-%m-%d %H:%M:%S"), item[1], item[2]).__dict__)
        return list

    #查找最近一个小时的数据
    def search_last_hour(self):
        list = []
        sql = "SELECT * FROM `data` WHERE time > DATE_SUB(NOW(), INTERVAL 1 HOUR)"
        results = self.common_search(sql)
        for item in results:
            list.append(sql_dict(item[0].strftime("%Y-%m-%d %H:%M:%S"), item[1], item[2]).__dict__)
        return list

    #查找所有数据
    def search_all(self):
        list = []
        sql = "SELECT * FROM `data`"
        results = self.common_search(sql)
        for item in results:
            list.append(sql_dict(item[0].strftime("%Y-%m-%d %H:%M:%S"), item[1], item[2]).__dict__)
        return list

    # select *  from data order by time LIMIT 1200 获取最近1200条

# 使用范例
# mysql().insert_data({'v1':2.8,'v2':1.3,'v3':0.1})
# print(mysql().search_by_hour('2021-03-16 13:00'))
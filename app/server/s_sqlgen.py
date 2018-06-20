from pymysql import *

class TftpMysql():
    def __init__(self,host,port,db,user,passwd,
                 charset="utf8"):
        self.host = host
        self.port = port
        self.db = db
        self.user = user
        self.passwd = passwd
        self.charset = charset

    def Tables(self):
        sql_select = "create table message(name varchar(10),\
                        password varchar(10));"
        self.cursor.execute(sql_select)
        sql_select = "insert into message values('root','123')"
        self.cursor.execute(sql_select)  

    def open(self):
        self.conn = connect(host=self.host,port=
                    self.port,db=self.db,user=self.user,
                    passwd=self.passwd,
                    charset=self.charset)
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def mysqlLogin(self,name,password):
        ret = 0
        sql_select = "select name,password from message where name=%s and password=%s;"
        l = (name,password)
        self.cursor.execute(sql_select,l)
        data = self.cursor.fetchone()
        ret = 1 if not data else 0
        return ret

    def mysqlRigester(self,name,password):
        ret = 0
        sql_select = "select name from message where name=%s;"
        self.cursor.execute(sql_select,name)
        data = self.cursor.fetchone()
        if not data:
            sql_select = "insert into message(name,password) value(%s,%s)"
            l = (name,password)
            self.cursor.execute(sql_select,l)
            ret = 0
        else:
            ret = 1
        return ret

if __name__ == '__main__':
    test = TftpMysql("localhost", 3306, "user", "root", "xiao404040")
    test.open()
    Ret = test.mysqlRigester('hxw','123456')
    A = test.mysqlLogin('hxw','123456')
    test.close()
    print(Ret)
    print(A)

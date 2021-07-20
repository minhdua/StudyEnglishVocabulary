import mysql.connector
from mysql.connector.errors import DatabaseError, IntegrityError, InternalError


class Connector:
    def __init__(self,host='localhost',user='root',password='hienvt9',database='hacknao1500'):
        self.db    =    mysql.connector.connect(host = host,
                            user = user,
                            password = password,
                            database = database)
        self.my_cursor = self.db .cursor()

    def execute(self,sql):
        self.my_cursor.execute(sql)

    def fetchall(self,sql):
        try:
            self.execute(sql)
            return self.my_cursor.fetchall()
        except IntegrityError as e:
            input(e)
        except DatabaseError as e:
            print(e)
        except Exception as e:
            print(e)

    def fetchone(self,sql):
        try:
            self.execute(sql)
            return self.my_cursor.fetchone()
        except IntegrityError as e:
            print(e)
        except DatabaseError as e:
            print(e)

    def commit(self,sql):
        try:
            self.execute(sql)
            self.db.commit()
        except InternalError as e:
            input(e)
        except DatabaseError as e:
            print(e)
        except Exception as e:
            print(e)

    def callproc(self):
        args =[0,1,2]
        result_args = self.my_cursor.callproc('general_infor', args)
        return result_args


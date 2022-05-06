import os
import sqlite3


class SqlitePool:
    __file__ = "./model.db"
    db_file = os.path.realpath(__file__)

    def __enter__(self):
        self.conn = sqlite3.connect(SqlitePool.db_file)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()


class InitDB:
    @staticmethod
    def query(sql, data=None):
        with SqlitePool() as db:
            if data:
                result = db.cursor.execute(sql, data).fetchall()
            else:
                result = db.cursor.execute(sql).fetchall()
            if result:
                return result

    @staticmethod
    def create(sql, data=None):
        try:
            with SqlitePool() as db:
                if data:
                    db.cursor.execute(sql, data)
                else:
                    db.cursor.execute(sql)
                db.conn.commit()
                return True
        except Exception as e:
            print(e)
            return False


def init_table():
    info_sql = "create table if not exists info(_id INTEGER PRIMARY KEY AUTOINCREMENT,l_name VARCHAR NOT NULL,img VARCHAR NOT NULL,model VARCHAR NOT NULL,name VARCHAR NOT NULL);"
    init_db.create(info_sql)
    label_sql = "CREATE TABLE if not exists LABEL(ID INTEGER PRIMARY KEY AUTOINCREMENT,NAME  VARCHAR  UNIQUE)"
    init_db.create(label_sql)
    path_sql = "CREATE TABLE if not exists PATH(ID INTEGER PRIMARY KEY AUTOINCREMENT,NAME  VARCHAR  UNIQUE)"
    init_db.create(path_sql)


init_db = InitDB()

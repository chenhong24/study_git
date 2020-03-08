import pymysql
from common.handleconfig import conf


class DB:
    def __init__(self):
        self.conn = pymysql.connect(host=conf.get("db", "host"),
                                    port=conf.getint("db", "port"),
                                    user=conf.get("db", "user"),
                                    password=conf.get("db", "pwd"),
                                    charset=conf.get("db", "charset"),
                                    cursorclass=pymysql.cursors.DictCursor

                                    )
        self.cur = self.conn.cursor()

    def find_one(self, sql):
        self.conn.commit()
        self.cur.execute(sql)
        data = self.cur.fetchone()
        return data

    def find_all(self, sql):
        self.conn.commit()
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def find_count(self, sql):
        """返回查询数据的条数"""
        self.conn.commit()
        return self.cur.execute(sql)

    def close(self):
        self.cur.close()
        self.conn.close()

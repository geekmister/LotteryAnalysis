import pymysql as mysql
import json


DATA_CONFIG = {}
with open('config.json') as config_file:
    DATA_CONFIG = json.load(config_file)["db"]


class DBManager:
    def __init__(self):

        self.conn = mysql.connect(
            host=DATA_CONFIG["host"],
            port=DATA_CONFIG["port"],
            user=DATA_CONFIG["name"],
            password=DATA_CONFIG["password"],
            database=DATA_CONFIG["database"],
        )
        self.cursor = self.conn.cursor()


    def insert(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()


    def queryone(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    
    def close(self):
        self.cursor.close()
        self.conn.close()


    
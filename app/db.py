import os
import psycopg2
from psycopg2.extras import execute_values, RealDictCursor

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_USER_PWD = os.getenv('DB_USER_PWD')


class DB(object):
    def __init__(self):
        self.connection = psycopg2.connect(
            host=DB_HOST
        )
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def get_cursor(self):
        return getattr(self, 'cursor')

    def execute_query(self, query, *params):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()

    def q_result(self, fields, serial=False):
        response = self.cursor.fetchall()
        result = []
        for _row in response:
            new_dict, old_dict = dict(), dict(_row)
            for key in fields:
                new_dict[key] = old_dict[key]
            result.append(new_dict)
        if len(fields) == 1 and serial:
            result = list(map(lambda row: row[fields[0]], result))
        return result

    def close(self):
        self.cursor.close()
        self.connection.close()

    def query_result(self, keywords):
        query = "select keywords, link from query_history where keywords=%s order by created desc limit 5"
        self.execute_query(query, keywords)
        return self.q_result(fields=['link'], serial=True)

    def query_history(self, keywords):
        query = "select distinct keywords from query_history where keywords like '%%%s%%'" % keywords
        self.execute_query(query)
        return self.q_result(fields=['keywords'], serial=True)

    def save_result(self, keywords, result):
        result = [(keywords, link)for link in result]
        query = "insert into query_history (keywords, link) values %s"
        execute_values(self.cursor, query, result)
        self.connection.commit()


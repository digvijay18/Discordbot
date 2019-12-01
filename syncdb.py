import os
import psycopg2
from psycopg2.extras import RealDictCursor

from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DATABASE_URL')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_USER_PWD = os.getenv('DB_USER_PWD')


def create_database():
    connection = psycopg2.connect(
        host=DB_HOST, user=DB_USER, password=DB_USER_PWD, database=DB_NAME
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute('create table query_history ('
                   'keywords varchar(255),'
                   'link varchar(255),'
                   'created timestamp not null default current_timestamp)')
    connection.commit()
    cursor.close()
    connection.close()


if __name__ == '__main__':
    create_database()

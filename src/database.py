import psycopg2
import psycopg2.extras
from loguru import logger

from config import DATABASE_URL


class Database:
    temp = DATABASE_URL.split('//')[1].split(':')
    username = temp[0]
    password = temp[1].split('@')[0]
    host = temp[1].split('@')[1].split('/')[0]
    port = temp[2].split('/')[0]
    database = temp[2].split('/')[1]

    def __init__(self) -> None:
        self.conn = None
        self.connect()

    def connect(self):
        if self.conn is not None:
            self.conn.close()
        self.conn = psycopg2.connect(
            f'user={self.username} password={self.password} host={self.host} port={self.port} dbname={self.database}')
        logger.info("Connnect to database")
        self.cursor = self.conn.cursor()

    def __execute(self, func: callable, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            self.connect()
            return func()

    def __create_table(self):
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS posts (game_id INTEGER, last_post_id INTEGER)')
        self.conn.commit()
        logger.info("Created table")

    def __set_last_post(self, game_id, last_post_id):
        self.cursor.execute(
            f'INSERT INTO posts (game_id, last_post_id) VALUES ({game_id}, {last_post_id})')
        self.conn.commit()

    def __update_last_post(self, game_id, post_id):
        self.cursor.execute(
            f'UPDATE posts SET last_post_id = {post_id} WHERE game_id = {game_id}')
        self.conn.commit()

    def __update_or_create_last_post(self, game_id, post_id):
        self.cursor.execute(
            f'SELECT last_post_id FROM posts WHERE game_id = {game_id}')
        if self.cursor.rowcount:
            self.__update_last_post(game_id, post_id)
        else:
            self.__set_last_post(game_id, post_id)

    def __get_last_post(self, game_id):
        self.cursor.execute(
            f'SELECT last_post_id FROM posts WHERE game_id = {game_id}')
        return None if self.cursor.rowcount == 0 else self.cursor.fetchone()[0]

    def create_table(self):
        return self.__execute(self.__create_table)

    def update_last_post(self, game_id, post_id):
        return self.__execute(self.__update_last_post, game_id, post_id)

    def set_last_post(self, game_id, last_post_id):
        return self.__execute(self.__set_last_post, game_id, last_post_id)

    def get_last_post(self, game_id):
        return self.__execute(self.__get_last_post, game_id)

    def update_or_create_last_post(self, game_id, post_id):
        return self.__execute(self.__update_or_create_last_post, game_id, post_id)

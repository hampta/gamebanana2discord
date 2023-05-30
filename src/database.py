from config import DatabaseConfig as db_config
from loguru import logger

if db_config.database_type == "sqlite":
    import sqlite3 

if db_config.database_type == "postgres":
    import psycopg2

class Database:
    def __init__(self) -> None:
        self.conn = None
        self.connect()

    def connect(self):
        if self.conn is not None:
            self.conn.close()
        if db_config.database_type == "sqlite":
            self.conn = sqlite3.connect(db_config.database)
        if db_config.database_type == "postgres":
            self.conn = psycopg2.connect(
                f'user={db_config.username} password={db_config.password} host={db_config.host} port={db_config.port} dbname={db_config.database}')
        logger.info("Connnect to database")
        self.cursor = self.conn.cursor()
        # self.conn = psycopg2.connect(
        #     f'user={db_config.username} password={db_config.password} host={db_config.host} port={db_config.port} dbname={db_config.database}')
        # logger.info("Connnect to database")
        # self.cursor = self.conn.cursor()

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

    def __get_last_posts(self):
        self.cursor.execute(
            'SELECT game_id, last_post_id FROM posts')
        return self.cursor.fetchall()

    def __add_game(self, game_id):
        self.cursor.execute(
            f'INSERT INTO posts (game_id, last_post_id) VALUES ({game_id}, 0)')
        self.conn.commit()

    def __get_games(self):
        self.cursor.execute(
            'SELECT game_id FROM posts')
        return self.cursor.fetchall()

    def create_table(self):
        return self.__execute(self.__create_table)

    def update_last_post(self, game_id, post_id):
        return self.__execute(self.__update_last_post, game_id, post_id)

    def set_last_post(self, game_id, last_post_id):
        return self.__execute(self.__set_last_post, game_id, last_post_id)

    def get_last_post(self, game_id):
        return self.__execute(self.__get_last_post, game_id)

    def get_last_posts(self):
        return self.__execute(self.__get_last_posts)

    def update_or_create_last_post(self, game_id, post_id):
        return self.__execute(self.__update_or_create_last_post, game_id, post_id)

    def add_games(self, game_id):
        return self.__execute(self.__add_game, game_id)
    
    def get_games(self):
        return self.__execute(self.__get_games)
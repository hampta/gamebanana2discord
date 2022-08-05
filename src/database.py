import psycopg2
import psycopg2.extras
from loguru import logger

from config import DATABASE_URL

temp = DATABASE_URL.split('//')[1].split(':')
username = temp[0]
password = temp[1].split('@')[0]
host = temp[1].split('@')[1].split('/')[0]
port = temp[2].split('/')[0]
database = temp[2].split('/')[1]
del temp

conn = psycopg2.connect(
    f'user={username} password={password} host={host} port={port} dbname={database}')
logger.info("Connected to database")
cursor = conn.cursor()


def create_table():
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS posts (game_id INTEGER, last_post_id INTEGER)')
    conn.commit()


def set_last_post(game_id, last_post_id):
    cursor.execute(
        f'INSERT INTO posts (game_id, last_post_id) VALUES ({game_id}, {last_post_id})')
    conn.commit()


def update_last_post(game_id, post_id):
    cursor.execute(
        f'UPDATE posts SET last_post_id = {post_id} WHERE game_id = {game_id}')
    conn.commit()


def get_last_post(game_id):
    cursor.execute(f'SELECT last_post_id FROM posts WHERE game_id = {game_id}')
    return None if cursor.rowcount == 0 else cursor.fetchone()[0]

from time import sleep

from loguru import logger

from config import GAMES_ID, TIME_SLEEP
from src.database import (create_table, get_last_post, set_last_post,
                      update_last_post)
from src.discord import send_to_discord_webhook
from src.gamebanana import get_feed, get_bulk_game_names

logger = logger.bind(name='main')


def check_feed():
    try:
        for game_id in GAMES_ID:
            logger.info(f"Processing game {game_id}")
            feed = get_feed(game_id)
            last_post = get_last_post(game_id)
            if last_post is None:
                logger.info(f"No last post for game {game_id}")
                set_last_post(game_id, feed[0]["_tsDateAdded"])
                send_to_discord_webhook(feed[0], game_id)
                continue
            for post in feed:
                if post['_tsDateAdded'] > last_post:
                    logger.info(f"New post: {post['_tsDateAdded']}")
                    send_to_discord_webhook(post, game_id)
                    update_last_post(game_id, post['_tsDateAdded'])
    except Exception as e:
        logger.error(e)
        sleep(5)
        check_feed()


def main():
    while True:
        check_feed()
        logger.info(f"Sleeping for {TIME_SLEEP} minutes")
        sleep(TIME_SLEEP)


if __name__ == "__main__":
    logger.info("Starting...")
    games = get_bulk_game_names(GAMES_ID)
    games_str = ", ".join(games)
    logger.info(f"Games: {games_str}")
    create_table()
    main()

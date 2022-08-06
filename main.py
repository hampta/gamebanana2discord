from time import sleep

from loguru import logger

from config import GAMES_ID, TIME_SLEEP
from src.database import Database
from src.discord import send_to_discord_webhook
from src.gamebanana import GameBanana

db = Database()
gb = GameBanana(GAMES_ID)

def check_feed():
    try:
        for game_id in GAMES_ID:
            logger.info(f"Processing game {game_id}")
            feed = gb.get_feed(game_id)
            last_post = db.get_last_post(game_id)
            for post in feed[::-1]:
                if last_post is None or post['_tsDateAdded'] > last_post:
                    logger.info(f"New post: {post['_tsDateAdded']}")
                    post_info = gb.get_mod_info(post["_sModelName"], post["_idRow"])
                    game = next(item for item in gb.games if item["_idRow"] == game_id)
                    send_to_discord_webhook(post_info, game['_sName'], game['_sIconUrl'], post["_sSingularTitle"])
                    db.update_or_create_last_post(game_id, post['_tsDateAdded'])
    except Exception as e:
        logger.exception(e)
        sleep(5)
        check_feed()


def main():
    while True:
        check_feed()
        logger.info(f"Sleeping for {TIME_SLEEP} seconds")
        sleep(TIME_SLEEP)


if __name__ == "__main__":
    logger.info("Starting...")
    games = [game["_sName"] for game in gb.games]
    logger.info(f"Games: {', '.join(games)}")
    db.create_table()
    main()

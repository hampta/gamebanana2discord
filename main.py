from time import sleep
from threading import Thread
from loguru import logger

from config import GAMES_ID, TIME_SLEEP, REPOST_SUBMISSIONS
from src.database import Database
from src.discord import Discord
from src.gamebanana import GameBanana

db = Database()
discord = Discord()

def check_game(game_id, last_post):
    logger.info(f"Processing game {game_id}")
    feed = gb.get_feed(game_id)
    game = gb.games[game_id]
    for post in feed[::-1]:
        if last_post is None or post['_tsDateAdded'] > last_post and post['_sSingularTitle'] in REPOST_SUBMISSIONS:
            logger.debug(f"New post: {post['_tsDateAdded']}")
            post_info = gb.get_mod_info(
                post["_sModelName"], post["_idRow"])
            #game = [item for item in gb.games if item["_idRow"] == game_id]
            discord.send_to_discord_webhook(
                post_info, game['_sName'], game['_sIconUrl'], post["_sSingularTitle"])
            db.update_or_create_last_post(
                game_id, post['_tsDateAdded'])

def check_feed():
    try:
        last_posts = db.get_last_posts()
        logger.info(f"Checking {last_posts} games")
        for game_id, last_post in last_posts:
            logger.info(f"Checking game {game_id} with last post {last_post}")
            Thread(target=check_game, args=(game_id, last_post)).start()
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
    db.create_table()
    games = [int(item) for (item,) in db.get_games()]
    for game in GAMES_ID:
        if int(game) not in games:
            db.add_games(game)
    gb = GameBanana(games)
    game_names = [game["_sName"] for game in gb.games.values()]
    logger.info(f"Games: {', '.join(game_names)}")
    main()

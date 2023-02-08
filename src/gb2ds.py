from time import sleep
from threading import Thread
from loguru import logger

from config import GAMES_ID, TIME_SLEEP, REPOST_SUBMISSIONS
from src.database import Database
from src.services.discord import Discord
from src.services.gamebanana import GameBanana


class Gamebanana2Discord():
    db = Database()
    discord = Discord()

    def __init__(self):
        logger.info("Starting...")
        self.db.create_table()
        games = [int(item) for (item,) in self.db.get_games()]
        for game in GAMES_ID:
            if int(game) not in games:
                self.db.add_games(game)
        self.gb = GameBanana(games)
        self.game_names = [game["_sName"] for game in self.gb.games.values()]
        logger.info(f"Games: {', '.join(self.game_names)}")

    def start(self):
        while True:
            self.check_feed()
            logger.info(f"Sleeping for {TIME_SLEEP} seconds")
            sleep(TIME_SLEEP)

    def check_game(self, game_id, last_post):
        logger.info(f"Processing game {game_id}")
        feed = self.gb.get_feed(game_id)
        game = self.gb.games[game_id]
        for post in feed[::-1]:
            if last_post is None or post['_tsDateAdded'] > last_post and post['_sSingularTitle'] in REPOST_SUBMISSIONS:
                logger.debug(f"New post: {post['_tsDateAdded']}")
                post_info = self.gb.get_mod_info(
                    post["_sModelName"], post["_idRow"])
                self.discord.send_to_discord_webhook(
                    post_info, game['_sName'], game['_sIconUrl'], post["_sSingularTitle"])
                self.db.update_or_create_last_post(
                    game_id, post['_tsDateAdded'])

    def check_feed(self):
        try:
            last_posts = self.db.get_last_posts()
            logger.info(f"Checking {', '.join(self.game_names)}")
            for game_id, last_post in last_posts:
                Thread(target=self.check_game, args=(
                    game_id, last_post)).start()
        except Exception as e:
            logger.exception(e)
            sleep(5)
            self.check_feed()

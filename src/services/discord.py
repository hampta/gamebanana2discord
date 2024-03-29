from time import sleep

import requests 
from config import WEBHOOK_URL
from loguru import logger
from time import sleep
from src.utils import create_embed


class Discord:

    def __init__(self):
        self.rate_limit = 0

    def send_to_discord_webhook(self, post: dict, section: str):
        if self.rate_limit > 0:
            sleep(self.rate_limit)
        embed: dict = create_embed(post, section)
        result: requests.Response = requests.post(WEBHOOK_URL, json=embed)
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            if result.status_code == 429:
                self.rate_limit = int(result.headers["Retry-After"]) / 1000
                logger.info(
                    f"Rate limit exceeded, sleeping for {self.rate_limit} seconds")
                sleep(self.rate_limit)
                self.send_to_discord_webhook(post, section)
            else:
                logger.exception(err)
        sleep(5)

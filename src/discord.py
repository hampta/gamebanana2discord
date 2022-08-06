from time import sleep

import requests
from config import WEBHOOK_URL
from loguru import logger

from src.utils import create_embed


def send_to_discord_webhook(post, game, icon, section):
    embed = create_embed(post, game, icon, section)
    result = requests.post(WEBHOOK_URL, json=embed)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if result.status_code == 429:
            time = int(result.headers['Retry-After']) / 1000
            logger.info(
                f"Rate limit exceeded, sleeping for {time} seconds")
            sleep(time)
            send_to_discord_webhook(post, game, icon, section)
        else:
            logger.exception(err)
    else:
        logger.debug(
            f"Payload delivered successfully, code {result.status_code}.")

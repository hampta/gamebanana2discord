from time import sleep

import requests
from config import WEBHOOK_URL
from loguru import logger

from src.utils import create_embed

logger = logger.bind(name='discord')


def send_to_discord_webhook(post, game, icon, section):
    embed = create_embed(post, game, icon, section)
    result = requests.post(WEBHOOK_URL, json=embed)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if result.status_code == 429:
            logger.info(
                f"Rate limit exceeded, sleeping for {result.headers['Retry-After']} milliseconds")
            sleep(int(result.headers['Retry-After']) / 1000)
            send_to_discord_webhook(post, game, icon, section)
        logger.exception(err)
    else:
        logger.debug(
            f"Payload delivered successfully, code {result.status_code}.")

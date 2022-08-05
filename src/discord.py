import requests
from config import WEBHOOK_URL
from loguru import logger

from src.utils import create_embed

logger = logger.bind(name='discord')


def send_to_discord_webhook(post, game_id):
    embed = create_embed(post, game_id)
    result = requests.post(WEBHOOK_URL, json=embed)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.error(err)
    else:
        logger.info(
            f"Payload delivered successfully, code {result.status_code}.")

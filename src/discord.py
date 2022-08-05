from datetime import datetime
from loguru import logger

import requests
from loguru import logger

from config import DOWNLOAD_ICON, WEBHOOK_URL
from src.gamebanana import get_download_url, get_game_info
from src.utils import convert_article

logger = logger.bind(name='discord')


def send_to_discord_webhook(post, game_id):
    #data = {"content": f"{post['_sArticle']} - {post['_sProfileUrl']}", "username": post['_aOwner']['_sUsername'], "avatar_url": post['_aOwner']['_sAvatarUrl'], "tts": False}
    game_name, game_icon = get_game_info(game_id)
    data = {
        "username": game_name,
        "avatar_url": game_icon,
        "embeds": [
            {
                "title": post['_sName'],
                "description": convert_article(post['_sArticle']),
                "url": post['_sProfileUrl'],
                "color": 0xffff00,
                "author": {
                    "name": "Download",
                    "url": get_download_url(post['_idItemRow']),
                    "icon_url": DOWNLOAD_ICON,
                },
                "image": {
                    "url": f"https://gamebanana.com/mods/embeddables/{post['_idItemRow']}?type=sd_image"
                },
                "footer": {
                    "text": post['_aOwner']['_sUsername'],
                    "icon_url": post['_aOwner']['_sAvatarUrl'],
                },
                "fields": [
                    {
                        "name": "Category",
                        "value": post['_aRootCategory']['_sName'],
                        "inline": True
                    },
                    {
                        "name": "Section",
                        "value": post['_aCategory']['_sName'],
                        "inline": True
                    },
                ],
                "timestamp": datetime.fromtimestamp(post['_tsDateAdded']).isoformat(),
            }
        ]
    }
    if post['_aSuperCategory']['_sName'] is not None:
        data['embeds'][0]['fields'].append(
            {
                "name": "Super Category",
                "value": post['_aSuperCategory']['_sName'],
                "inline": True
            }
        )
    if post['_aStudio']['_sStudioName'] is not None:
        data['embeds'][0]['fields'].append(
            {
                "name": "Studio",
                "value": post['_aStudio']['_sStudioName'],
                "inline": True
            }
        )
    result = requests.post(WEBHOOK_URL, json=data)
    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        logger.error(err)
    else:
        logger.info(
            f"Payload delivered successfully, code {result.status_code}.")

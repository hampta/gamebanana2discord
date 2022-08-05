import requests
from loguru import logger

from config import BASE_URL

logger = logger.bind(name='gamebanana')


def get_game_info(game_id) -> list:
    url = f"https://gamebanana.com/apiv9/Member/UiConfig?_sUrl=%2Fgames%2F{game_id}"
    response = requests.get(url).json()['_aGame']
    return response['_sName'], response['_sIconUrl']


def get_feed(game_id: int) -> str:
    url = f"{BASE_URL}/mods/games/{game_id}?api=SubmissionsListModule"
    feed = requests.get(url).json()["_aCellValues"]
    feed.sort(key=lambda x: -x['_tsDateAdded'])
    return feed


def get_download_url(id) -> str:
    request = requests.get(
        f"https://gamebanana.com/apiv9/Mod/{id}/DownloadPage")
    if request.text != '':
        return request.json()['_aFiles'][0]['_sDownloadUrl']
    return None


def get_bulk_game_names(ids) -> list:
    return [get_game_info(id)[0] for id in ids]

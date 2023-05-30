import requests
from config import API_URL


class GameBanana:

    def __init__(self, games_ids) -> None:
        self.games: dict = self.get_bulk_games(games_ids)

    def get_game_info(self, game_id) -> dict:
        request: requests.Response = requests.get(f"{API_URL}/Member/UiConfig?_sUrl=%2Fgames%2F{game_id}")
        return request.json()

    def get_feed(self, game_id: int, page=1, perpage=50, mode="new") -> dict:
        return requests.get(f"{API_URL}/Game/{game_id}/Subfeed?_nPage={page}&_nPerpage={perpage}&_sSort={mode}").json()["_aRecords"]

    def get_mod_info(self, submission_type, id) -> dict:
        return requests.get(f"{API_URL}/{submission_type}/{id}/ProfilePage").json()

    def get_bulk_games(self, ids) -> dict:
        tmp: list = [self.get_game_info(id)["_aGame"] for id in ids]
        return {int(item["_idRow"]): item for item in tmp}

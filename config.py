from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_URL: str = "https://gamebanana.com/apiv10"
GAMES_ID: list[int] = [int(i) for i in getenv("GAMES_ID").replace(" ", "").split(",")]
DOWNLOAD_ICON: str = "https://cdn.discordapp.com/attachments/942477980167446538/1004980354819559435/icon_sheet.png"
DATABASE_URL: str = getenv("DATABASE_URL")
WEBHOOK_URL: str = getenv("WEBHOOK_URL")
TIME_SLEEP: int = int(getenv("TIME_SLEEP") or 15 * 60)
REPOST_SUBMISSIONS: list[str] = getenv("REPOST_SUBMISSIONS").split(",")


@dataclass
class DatabaseConfig:
    temp = DATABASE_URL.split("//")[1].split(":")
    database_type = DATABASE_URL.split("://")[0]
    if database_type == "sqlite":
        database = temp[0].split("/")[1]
    else:
        username = temp[0]
        password = temp[1].split("@")[0]
        host = temp[1].split("@")[1].split("/")[0]
        port = temp[2].split("/")[0]
        database = temp[2].split("/")[1]
    del temp
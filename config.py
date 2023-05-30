from os import getenv

API_URL:str = "https://gamebanana.com/apiv10"
GAMES_ID: list[int] = [int(i) for i in getenv("GAMES_ID").replace(" ", "").split(",")]
DOWNLOAD_ICON: str = 'https://cdn.discordapp.com/attachments/942477980167446538/1004980354819559435/icon_sheet.png'
DATABASE_URL: str = getenv('DATABASE_URL')
WEBHOOK_URL: str = getenv('WEBHOOK_URL')
TIME_SLEEP: int = int(getenv('TIME_SLEEP') or 15 * 60)
REPOST_SUBMISSIONS: list[str] = getenv('REPOST_SUBMISSIONS').split(',')
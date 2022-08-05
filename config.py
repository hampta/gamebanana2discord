from os import getenv


BASE_URL = "https://gamebanana.com"
GAMES_ID = getenv("GAMES_ID").replace(" ", "").split(",")
DOWNLOAD_ICON = 'https://cdn.discordapp.com/attachments/942477980167446538/1004980354819559435/icon_sheet.png'
DATABASE_URL = getenv('DATABASE_URL')
WEBHOOK_URL = getenv('WEBHOOK_URL')
TIME_SLEEP = int(getenv('TIME_SLEEP')) or 15 * 60
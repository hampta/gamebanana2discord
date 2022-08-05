from datetime import datetime

from bs4 import BeautifulSoup
from config import BASE_URL, DOWNLOAD_ICON

from src.gamebanana import get_download_url, get_game_info


def convert_article(v) -> str:
    bs = BeautifulSoup(v, 'html.parser')
    if bs.iframe:
        urls = [iframe.get('src') for iframe in bs.find_all('iframe')]
        return bs.text + '\n' + '\n'.join(urls)
    text = bs.get_text(' ', strip=True).replace('\n', '')
    if bs.span is not None:
        title = bs.span.text
        text = text.replace(title, '').strip()
        text = f"{title}\n{text}"
    return text

def cut_string(string, max_length):
    return f'{string[:max_length]}...' if len(string) > max_length else string

def create_embed(post, game_id):
    game_name, game_icon = get_game_info(game_id)
    description = convert_article(post['_sArticle'])
    description = cut_string(description, 256)
    embed: dict = {
        "username": game_name,
        "avatar_url": game_icon,
        "embeds": [
            {
                "title": post['_sName'],
                "description": description,
                "url": post['_sProfileUrl'],
                "color": 0xffff00,
                "author": {
                    "name": "Download",
                    "url": get_download_url(post['_idItemRow']),
                    "icon_url": DOWNLOAD_ICON,
                },
                "image": {
                    "url": f"{BASE_URL}/mods/embeddables/{post['_idItemRow']}?type=sd_image"
                },
                "footer": {
                    "text": post['_aOwner']['_sUsername'],
                    "icon_url": post['_aOwner']['_sAvatarUrl'],
                },
                "fields": [],
                "timestamp": datetime.fromtimestamp(post['_tsDateAdded']).isoformat(),
            }
        ]
    }
    embed["embeds"][0]["fields"].append(
        {
            "name": "Category",
            "value": post['_aRootCategory']['_sName'],
            "inline": True
        }
    )
    if post['_aSuperCategory']['_sName'] is not None and post['_aSuperCategory']['_sName'] != post['_aRootCategory']['_sName']:
        embed['embeds'][0]['fields'].append(
            {
                "name": "SubCategory",
                "value": post['_aSuperCategory']['_sName'],
                "inline": True
            }
        )
    embed["embeds"][0]["fields"].append(
        {
            "name": "Section",
            "value": post['_aCategory']['_sName'],
            "inline": True
        }
    )
    if post['_aStudio']['_sStudioName'] is not None:
        embed['embeds'][0]['fields'].append(
            {
                "name": "Studio",
                "value": post['_aStudio']['_sStudioName'],
                "inline": True
            }
        )
    return embed

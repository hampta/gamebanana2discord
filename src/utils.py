import math
from datetime import datetime
from typing import Tuple

from bs4 import BeautifulSoup

from config import DOWNLOAD_ICON


def convert_article(v: str) -> str:
    bs: BeautifulSoup = BeautifulSoup(v, "html.parser")
    if bs.iframe:
        urls: list = [iframe.get("src") for iframe in bs.find_all("iframe")]
        return bs.text + "\n" + "\n".join(urls)
    text: str = bs.get_text(" ", strip=True).replace("\n", "")
    if bs.span is not None:
        title: str = bs.span.text
        text = text.replace(title, "").strip()
        text = f"{title}\n{text}"
    return text


def convert_size(size_bytes: int) -> str:
    if size_bytes == 0:
        return "0B"
    size_name: Tuple[str, ...] = "B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"
    i: int = int(math.floor(math.log(size_bytes, 1024)))
    p: float = math.pow(1024, i)
    s: float = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"


def cut_string(string: str, max_length: int) -> str:
    return f"{string[:max_length]}..." if len(string) > max_length else string


def create_embed(post: dict, section: str) -> dict:
    description = convert_article(post["_sText"])
    description = cut_string(description, 256)
    embed: dict = {
        "username": post["_aGame"]["_sName"],
        "avatar_url": post["_aGame"]["_sIconUrl"],
        "embeds": [
            {
                "title": post["_sName"],
                "description": description,
                "url": post["_sProfileUrl"],
                "author": {},
                "color": 0x00ff00,
                "image": {
                    "url": f"{post['_aPreviewMedia']['_aImages'][0]['_sBaseUrl']}/{post['_aPreviewMedia']['_aImages'][0]['_sFile']}",
                },
                "footer": {
                    "text": post["_aSubmitter"]["_sName"],
                    "icon_url": post["_aSubmitter"]["_sAvatarUrl"],
                },
                "fields": [
                    {
                        "name": "Section",
                        "value": section,
                        "inline": True,
                    }
                ],
                "timestamp": datetime.fromtimestamp(post["_tsDateAdded"]).isoformat(),
            }
        ]
    }
    if "_aSuperCategory" in post:
        embed["embeds"][0]["fields"].append({
            "name": "Category",
            "value": post["_aSuperCategory"]["_sName"],
            "inline": True
        })
    embed["embeds"][0]["fields"].append({
        "name": "Sub-Category",
        "value": post["_aCategory"]["_sName"],
        "inline": True
    })
    if "_aStudio" in post:
        embed["embeds"][0]["fields"].append(
            {
                "name": "Studio",
                "value": post["_aStudio"]["_sName"],
                "inline": True
            }
        )
    if "_aFiles" in post:
        embed["embeds"][0]["author"] |= {
            "name": f"Download: {convert_size(post['_aFiles'][0]['_nFilesize'])}",
            "url": post["_aFiles"][0]["_sDownloadUrl"],
            "icon_url": DOWNLOAD_ICON,
        }
    if post["_sInitialVisibility"] != "show":
        embed["embeds"][0]["color"] = 0xff0000
        embed["embeds"][0]["image"] |= {
            "url": "https://cdn.discordapp.com/attachments/942477980167446538/1005394994653311016/unknown.png"}
    return embed

import json
import subprocess
import re

FILE_PATH = r"E:\PPP\Public\data\episodes.json"


def get_views(url):
    try:
        result = subprocess.check_output(
            ["yt-dlp", "--print", "%(view_count)s", url],
            text=True
        ).strip()

        return int(result)

    except:
        return 0


with open(FILE_PATH, "r", encoding="utf-8") as f:
    episodes = json.load(f)

for ep in episodes:

    yt_url = ep.get("yt")

    if not yt_url:
        continue

    views = get_views(yt_url)

    ep["views"] = views

    print(f"{ep['id']} -> {views} views")


with open(FILE_PATH, "w", encoding="utf-8") as f:
    json.dump(episodes, f, indent=2, ensure_ascii=False)

print("Done! Views updated.")
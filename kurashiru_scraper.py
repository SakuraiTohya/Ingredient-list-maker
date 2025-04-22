import requests
from bs4 import BeautifulSoup
import json

def get_recipe_info_from_kurashiru(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print("ページ取得失敗")
        return None

    soup = BeautifulSoup(res.text, "html.parser")
    scripts = soup.find_all("script", type="application/ld+json")

    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get("@type") == "Recipe":
                ingredients = data.get("recipeIngredient", [])
                yield_info = data.get("recipeYield", "")  # ←ここ
                return {
                    "ingredients": ingredients,
                    "yield": yield_info  # "2人前" みたいな文字列
                }
        except:
            continue
    return None


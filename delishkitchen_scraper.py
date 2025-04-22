import requests
from bs4 import BeautifulSoup

def get_recipe_info_from_delishkitchen(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print("ページ取得失敗")
        return None

    soup = BeautifulSoup(res.text, "html.parser")

    # --- 材料 ---
    ingredients = []
    ingredient_items = soup.select("ul.ingredient-list li.ingredient")
    for item in ingredient_items:
        name_elem = item.select_one("a.ingredient-name, span.ingredient-name")
        amount_elem = item.select_one("span.ingredient-serving")
        name = name_elem.text.strip() if name_elem else ""
        amount = amount_elem.text.strip() if amount_elem else ""
        if name:
            ingredients.append(f"{name} {amount}".strip())

    # --- 何人前の情報（【2人分】など） ---
    yield_info = ""
    yield_elem = soup.select_one("span.recipe-serving span")
    if yield_elem:
        yield_info = yield_elem.text.strip()

    return {
        "ingredients": ingredients,
        "yield": yield_info
    }



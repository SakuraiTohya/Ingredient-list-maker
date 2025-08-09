"""
Delish Kitchen scraper - デリッシュキッチンからレシピ情報を取得するモジュール
"""

from typing import Any, Dict, Optional

import requests
from bs4 import BeautifulSoup


def get_recipe_info_from_delishkitchen(url: str) -> Optional[Dict[str, Any]]:
    """
    デリッシュキッチンのレシピURLから材料情報と人数情報を取得する

    Args:
        url (str): デリッシュキッチンのレシピURL

    Returns:
        Optional[Dict[str, any]]: レシピ情報（材料リストと人数）、失敗時はNone
    """
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            print(f"ページ取得失敗: ステータスコード {res.status_code}")
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

        return {"ingredients": ingredients, "yield": yield_info}

    except requests.RequestException as e:
        print(f"リクエストエラー: {e}")
        return None
    except Exception as e:
        print(f"予期しないエラー: {e}")
        return None

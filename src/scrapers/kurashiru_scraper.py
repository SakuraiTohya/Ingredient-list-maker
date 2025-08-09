"""
Kurashiru scraper - クラシルからレシピ情報を取得するモジュール
"""

import requests
from bs4 import BeautifulSoup
import json
from typing import Optional, Dict, List


def get_recipe_info_from_kurashiru(url: str) -> Optional[Dict[str, any]]:
    """
    クラシルのレシピURLから材料情報と人数情報を取得する
    
    Args:
        url (str): クラシルのレシピURL
        
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
        scripts = soup.find_all("script", type="application/ld+json")

        for script in scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and data.get("@type") == "Recipe":
                    ingredients = data.get("recipeIngredient", [])
                    yield_info = data.get("recipeYield", "")
                    return {
                        "ingredients": ingredients,
                        "yield": yield_info
                    }
            except (json.JSONDecodeError, TypeError):
                continue
                
    except requests.RequestException as e:
        print(f"リクエストエラー: {e}")
        return None
    except Exception as e:
        print(f"予期しないエラー: {e}")
        return None
        
    return None

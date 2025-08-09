"""
メインアプリケーション - Streamlitアプリのメイン処理
"""

import streamlit as st
import sys
import os

# プロジェクトのルートディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.scrapers import get_recipe_info_from_kurashiru, get_recipe_info_from_delishkitchen
from src.utils import (
    parse_ingredient, combine_ingredients, format_ingredient_summary,
    extract_people_count
)
from src.utils.sheet_utils import write_to_spreadsheet
from collections import defaultdict
from typing import List, Tuple


def initialize_session_state() -> None:
    """セッション状態を初期化"""
    if "recipe_count" not in st.session_state:
        st.session_state.recipe_count = 1
    if "combined_list" not in st.session_state:
        st.session_state["combined_list"] = []
    if "extra_ingredients" not in st.session_state:
        st.session_state["extra_ingredients"] = []


def collect_recipe_inputs() -> Tuple[List[str], List[int], List[str]]:
    """レシピ入力を収集"""
    recipe_urls = []
    num_people = []
    recipe_names = []

    for i in range(st.session_state.recipe_count):
        st.markdown(f"### 🍽️ レシピ #{i+1}")
        name = st.text_input(f"料理名", key=f"recipe_title_{i}")
        cols = st.columns(2)
        with cols[0]:
            url = st.text_input(f"レシピURL ", key=f"url_{i}")
        with cols[1]:
            people = st.number_input(f"作りたい人数 ", min_value=1, step=1, value=2, key=f"people_{i}")

        if url:
            recipe_urls.append(url)
            num_people.append(people)
            recipe_names.append(name)

    return recipe_urls, num_people, recipe_names


def process_recipes(recipe_urls: List[str], num_people: List[int]) -> Tuple[List[str], List[str]]:
    """レシピを処理して材料リストを生成"""
    all_combined = defaultdict(float)
    extra_ingredients = []

    for url, target in zip(recipe_urls, num_people):
        try:
            if "kurashiru" in url:
                info = get_recipe_info_from_kurashiru(url)
            elif "delishkitchen" in url:
                info = get_recipe_info_from_delishkitchen(url)
            else:
                st.warning(f"未対応のURL形式です: {url}")
                continue

            if not info:
                st.warning(f"データ取得失敗: {url}")
                continue

            ingredients_raw = info["ingredients"]
            base_people = extract_people_count(info["yield"])
            multiplier = target / base_people if base_people > 0 else 1.0

            parsed = [parse_ingredient(item) for item in ingredients_raw]
            for name, amount, unit in parsed:
                if amount is None:
                    extra_ingredients.append(name)
                else:
                    all_combined[(name, unit)] += amount * multiplier

        except Exception as e:
            st.error(f"レシピ処理中にエラーが発生しました: {url} - {str(e)}")
            continue

    combined_list = format_ingredient_summary(all_combined)
    return combined_list, extra_ingredients


def render_ingredient_editor(combined_list: List[str], extra_ingredients: List[str]) -> Tuple[List[List[str]], List[str]]:
    """材料編集UIを表示"""
    st.subheader("✅ スプレッドシートに出力する材料を選んで編集")

    editable_items = []
    for i, line in enumerate(combined_list):
        parts = line.split()
        if len(parts) >= 2:
            name = parts[0]
            quantity = "".join(parts[1:])
            col1, col2, col3 = st.columns([3, 3, 2])
            with col1:
                new_name = st.text_input("材料名", value=name, key=f"ingredient_name_{i}")
            with col2:
                new_quantity = st.text_input("量", value=quantity, key=f"ingredient_amount_{i}")
            with col3:
                use_item = st.checkbox("出力", key=f"ingredient_use_{i}", value=True)
            if use_item:
                editable_items.append([new_name, new_quantity])

    selected_extras = []
    if extra_ingredients:
        st.subheader("😲 分量不明（適量・少々など）")
        for i, item in enumerate(extra_ingredients):
            col1, col2 = st.columns([6, 2])
            with col1:
                st.write(f"・{item}")
            with col2:
                use = st.checkbox("出力", value=True, key=f"extra_{i}")
            if use:
                selected_extras.append(item)

    return editable_items, selected_extras


def main():
    """メイン関数"""
    st.set_page_config(
        page_title="材料リスト作成ツール",
        page_icon="🍳",
        layout="wide"
    )
    
    st.title("🍳 材料リスト作成ツール")
    st.write(
        "レシピのURLを入力すると、必要な材料のリストを作成します。"
        "クラシルとデリッシュキッチンに対応しています。\n\n"
        "出力用のスプレッドシートがなくても材料の計算は可能です。"
        "分量は文字列、数値に対応してます。"
    )

    # セッション状態を初期化
    initialize_session_state()

    # レシピ入力欄の表示
    st.subheader("📅 レシピ入力")
    recipe_urls, num_people, recipe_names = collect_recipe_inputs()

    # レシピ追加ボタン
    if st.button("➕ レシピURLを追加"):
        st.session_state.recipe_count += 1
        st.rerun()

    # スプレッドシートURL
    st.subheader("📤 出力先スプレッドシートのURL")
    sheet_url = st.text_input("スプレッドシートURLを入力してください")

    # 実行ボタン
    if st.button("✅ 買い物リストを作成"):
        if not recipe_urls:
            st.warning("レシピURLを入力してください。")
            return

        with st.spinner("レシピを処理中..."):
            combined_list, extra_ingredients = process_recipes(recipe_urls, num_people)

        # セッションに保存
        st.session_state["combined_list"] = combined_list
        st.session_state["extra_ingredients"] = extra_ingredients
        st.session_state["show_editor"] = True
        st.rerun()

    # 材料表示と編集
    if st.session_state.get("show_editor", False):
        editable_items, selected_extras = render_ingredient_editor(
            st.session_state["combined_list"],
            st.session_state["extra_ingredients"]
        )

        if sheet_url and st.button("📤 この内容でスプレッドシートに出力する", key="submit_button"):
            try:
                with st.spinner("スプレッドシートに出力中..."):
                    write_to_spreadsheet(sheet_url, editable_items, selected_extras)
                st.success("✅ スプレッドシートに出力しました！")
            except Exception as e:
                st.error(f"出力に失敗しました: {str(e)}")


if __name__ == "__main__":
    main()

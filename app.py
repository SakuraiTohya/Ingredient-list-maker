import streamlit as st
from kurashiru_scraper import get_recipe_info_from_kurashiru
from delishkitchen_scraper import get_recipe_info_from_delishkitchen
from ingredient_utils import parse_ingredient, combine_ingredients, format_ingredient_summary
from collections import defaultdict
import re
import gspread
from google.oauth2.service_account import Credentials
# --- 人数抽出関数 ---
def extract_people_count(yield_text):
    match = re.search(r'(\d+)', yield_text)
    return int(match.group(1)) if match else 1

# --- スプレッドシート出力関数 ---
def write_to_spreadsheet(sheet_url, combined_list, extras):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )
    client = gspread.authorize(credentials)
    sheet = client.open_by_url(sheet_url)
    worksheet = sheet.sheet1

    worksheet.clear()
    worksheet.update(range_name='A1:B1', values=[["材料名", "分量"]])

    data = []
    for line in combined_list:
        parts = line.split()
        if len(parts) >= 2:
            name = parts[0]
            quantity = "".join(parts[1:])
            data.append([name, quantity])

    for item in extras:
        data.append([item, "適量または少々"])

    worksheet.update(range_name=f"A2:B{len(data)+1}", values=data)

# --- Streamlit アプリ本体 ---
st.title("🍳 材料リスト作成ツール")
st.write("レシピURLを入力すると、必要な材料のリストを作成します。クラシルとデリッシュキッチンに対応しています。")

# 初期化
if "recipe_count" not in st.session_state:
    st.session_state.recipe_count = 1

# レシピ追加ボタン
if st.button("➕ レシピURLを追加"):
    st.session_state.recipe_count += 1

# レシピ入力欄の表示
recipe_urls = []
num_people = []

st.subheader("📥 レシピ入力")
for i in range(st.session_state.recipe_count):
    cols = st.columns(2)
    with cols[0]:
        url = st.text_input(f"レシピURL #{i+1}", key=f"url_{i}")
    with cols[1]:
        people = st.number_input(f"作りたい人数 #{i+1}", min_value=1, step=1, value=2, key=f"people_{i}")

    if url:
        recipe_urls.append(url)
        num_people.append(people)

# スプレッドシートURL
st.subheader("📤 出力先スプレッドシートのURL")
sheet_url = st.text_input("スプレッドシートURLを入力してください")

# 実行ボタン
if st.button("✅ 買い物リストを作成"):
    all_combined = defaultdict(float)
    extra_ingredients = []

    for url, target in zip(recipe_urls, num_people):
        # --- URLに応じて使用する関数を分ける ---
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



    combined_list = format_ingredient_summary(all_combined)

    st.subheader("🛒 合計買い物リスト")
    for line in combined_list:
        st.write("-", line)

    if extra_ingredients:
        st.subheader("🧂 分量不明（適量・少々など）")
        for item in extra_ingredients:
            st.write("-", item)

    if sheet_url:
        write_to_spreadsheet(sheet_url, combined_list, extra_ingredients)
        st.success("✅ スプレッドシートに出力しました！")
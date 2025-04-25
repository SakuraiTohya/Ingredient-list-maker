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
        if isinstance(line, list) and len(line) == 2:
            name, quantity = line
        elif isinstance(line, str):
            parts = line.split()
            if len(parts) >= 2:
                name = parts[0]
                quantity = "".join(parts[1:])
            else:
                continue
        else:
            continue
        
        data.append([name, quantity])



    for item in extras:
        data.append([item, "適量または少々"])

    worksheet.update(range_name=f"A2:B{len(data)+1}", values=data)

# --- Streamlit アプリ本体 ---
st.title("🍳 材料リスト作成ツール")
st.write("レシピURLを入力すると、必要な材料のリストを作成します。クラシルとデリッシュキッチンに対応しています。\n\n出力シートがなくても材料計算は可能です。")

# 初期化
if "recipe_count" not in st.session_state:
    st.session_state.recipe_count = 1
if "combined_list" not in st.session_state:
    st.session_state["combined_list"] = []
if "extra_ingredients" not in st.session_state:
    st.session_state["extra_ingredients"] = []

# レシピ入力欄の表示
st.subheader("📅 レシピ入力")
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

# レシピ追加ボタン
if st.button("➕ レシピURLを追加"):
    st.session_state.recipe_count += 1

# スプレッドシートURL
st.subheader("📤 出力先スプレッドシートのURL")
sheet_url = st.text_input("スプレッドシートURLを入力してください")

# 実行ボタン
if st.button("✅ 買い物リストを作成"):
    all_combined = defaultdict(float)
    extra_ingredients = []

    for url, target in zip(recipe_urls, num_people):
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

    # セッションに保存
    st.session_state["combined_list"] = combined_list
    st.session_state["extra_ingredients"] = extra_ingredients
    st.session_state["show_editor"] = True

# 材料表示と編集
if st.session_state.get("show_editor", False):
    st.subheader("✅ スプレッドシートに出力する材料を選んで編集")

    editable_items = []
    for i, line in enumerate(st.session_state["combined_list"]):
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
    if "extra_ingredients" in st.session_state:
        st.subheader("😲 分量不明（適量・少々など）")
        for i, item in enumerate(st.session_state["extra_ingredients"]):
            col1, col2 = st.columns([6, 2])
            with col1:
                st.write(f"・{item}")
            with col2:
                use = st.checkbox("出力", value=True, key=f"extra_{i}")
            if use:
                selected_extras.append(item)

        if sheet_url and st.button("📤 この内容でスプレッドシートに出力する", key="submit_button"):
            write_to_spreadsheet(sheet_url, editable_items, selected_extras)
            st.success("✅ スプレッドシートに出力しました！")
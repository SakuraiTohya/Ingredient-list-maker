# 🛒 Ingredient List Maker for Recipes

このアプリは、**クラシル（kurashiru）とデリッシュキッチン（delish kitchen）**のレシピURLをもとに、  
複数人分の材料を合算して買い物リストを自動生成し、**Googleスプレッドシートに出力できる**Streamlitアプリです。

---

## 🚀 アプリを見る  
📍[アプリを使ってみる](https://ingredient-list-maker-dj2ly2z54u7u3wquznrcih.streamlit.app/)

---

## ✨ 主な機能

- 複数のレシピURLをまとめて入力可能  
- 各レシピごとに「作りたい人数」を設定  
- 材料を**人数に応じて自動的に合算**  
- 「適量」「少々」など分量不明な材料を別枠で表示  
- **スプレッドシートへの出力ON/OFF切り替え可能**  
- **材料名や分量を手動で編集可能**（カスタマイズ自由）

---

## 🛠 使い方

1. クラシルまたはデリッシュキッチンのレシピURLを入力  
2. 各レシピに対して「作りたい人数」を入力  
    - ※「○個分」などのレシピには非対応です  
3. 出力先のGoogleスプレッドシートのURLを入力  
    - ※自分が**編集権限を持つスプレッドシート**にしてください  
4. 必要に応じて「材料名」や「分量」の変更を行う  
5. 「✅ 買い物リストを作成」ボタンをクリック  
6. 結果が画面に表示され、**指定があればスプレッドシートにも自動で反映されます**

---

## 📦 使用技術

- [Streamlit](https://streamlit.io/)  
- [gspread](https://github.com/burnash/gspread)  
- Google Sheets API（+ Google Service Account）  
- Webスクレイピング（[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)）  
- Python標準ライブラリ（re, urllib, pandas など）

---

## 🔐 環境変数（Streamlit Secrets）

以下の形式で、Googleサービスアカウントの`credentials.json`を**Streamlit Secrets**に登録してください：

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service@your-project.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."

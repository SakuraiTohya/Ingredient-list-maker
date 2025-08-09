"""
設定ファイル - アプリケーション全体の設定値
"""

# スクレイピング用のHTTPヘッダー
HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# リクエストタイムアウト（秒）
REQUEST_TIMEOUT = 10

# Google Sheets API のスコープ
GOOGLE_SHEETS_SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# 単位が前に来る材料の単位リスト
PREFIX_UNITS = ["大さじ", "小さじ"]

# サポートするレシピサイト
SUPPORTED_SITES = {"kurashiru": "kurashiru.com", "delishkitchen": "delishkitchen.tv"}

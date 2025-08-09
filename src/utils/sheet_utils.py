"""
Spreadsheet utilities - Googleスプレッドシートへの出力機能
"""

from typing import List

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials


def write_to_spreadsheet(sheet_url: str, combined_list: List[List[str]], extras: List[str]) -> None:
    """
    Googleスプレッドシートに材料リストを出力

    Args:
        sheet_url (str): スプレッドシートのURL
        combined_list: 材料リスト（[材料名, 分量]のリスト）
        extras: 分量不明な材料のリスト

    Raises:
        Exception: スプレッドシートへの書き込みが失敗した場合
    """
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    try:
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"], scopes=scope
        )
        client = gspread.authorize(credentials)
        sheet = client.open_by_url(sheet_url)
        worksheet = sheet.sheet1

        # シートをクリアしてヘッダーを設定
        worksheet.clear()
        worksheet.update(range_name="A1:B1", values=[["材料名", "分量"]])

        data = []

        # 通常の材料を処理
        for line in combined_list:
            if len(line) >= 2:
                name, quantity = line[0], line[1]
                data.append([name, quantity])

        # 分量不明な材料を追加
        for item in extras:
            data.append([item, "適量または少々"])

        if data:
            worksheet.update(range_name=f"A2:B{len(data)+1}", values=data)

    except Exception as e:
        raise Exception(f"スプレッドシートへの書き込みに失敗しました: {str(e)}")

"""
Recipe utilities - レシピ関連のユーティリティ関数
"""

import re


def extract_people_count(yield_text: str) -> int:
    """
    レシピの分量表記から人数を抽出

    Args:
        yield_text (str): レシピの分量テキスト（例: "2人前"）

    Returns:
        int: 抽出された人数、見つからない場合は1
    """
    if not yield_text:
        return 1

    match = re.search(r"(\d+)", yield_text)
    return int(match.group(1)) if match else 1

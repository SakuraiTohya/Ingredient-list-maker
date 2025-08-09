"""
Ingredient utilities - 材料の解析・結合・フォーマット機能
"""

import re
from collections import defaultdict
from fractions import Fraction
from typing import Dict, List, Optional, Tuple


def convert_mixed_number(s: str) -> Optional[float]:
    """
    '2と1/2', '1/3', '1.5' などを float に変換

    Args:
        s (str): 変換する文字列

    Returns:
        Optional[float]: 変換された数値、変換失敗時はNone
    """
    s = s.replace("．", ".").replace("・", "/").replace("／", "/").strip()

    # 例: "2と1/2"
    match = re.match(r"(\d+)\s*と\s*(\d+)/(\d+)", s)
    if match:
        whole = int(match.group(1))
        frac = Fraction(int(match.group(2)), int(match.group(3)))
        return float(whole + frac)

    # 例: "1/2"
    match = re.match(r"(\d+)/(\d+)", s)
    if match:
        return float(Fraction(int(match.group(1)), int(match.group(2))))

    # 通常の数字
    try:
        return float(s)
    except ValueError:
        return None


def parse_ingredient(item: str) -> Tuple[str, Optional[float], str]:
    """
    材料文字列を解析して名前、分量、単位に分離

    Args:
        item (str): 材料の文字列（例: '醤油 大さじ1.5'）

    Returns:
        Tuple[str, Optional[float], str]: (材料名, 分量, 単位)
    """
    item = item.strip()

    # 正規表現：分数・小数・混合分数 すべて対応
    pattern = r"(.+?)\s+([^\d\s]*)(\d+(?:\.\d+)?(?:と\d+/\d+)?|(?:\d+/\d+))([^\d\s]*)$"
    match = re.match(pattern, item)
    if match:
        name = match.group(1).strip()
        prefix_unit = match.group(2).strip()
        number_part = match.group(3).strip()
        suffix_unit = match.group(4).strip()

        unit = prefix_unit or suffix_unit
        amount = convert_mixed_number(number_part)
        return name, amount, unit
    else:
        return str(item).strip(), None, ""


def combine_ingredients(
    parsed_ingredients: List[Tuple[str, Optional[float], str]], multiplier: float = 1.0
) -> Dict[Tuple[str, str], float]:
    """
    解析済み材料リストを結合して合計分量を計算

    Args:
        parsed_ingredients: 解析済み材料のリスト
        multiplier: 人数倍率

    Returns:
        Dict[Tuple[str, str], float]: (材料名, 単位) -> 合計分量の辞書
    """
    result: Dict[Tuple[str, str], float] = defaultdict(float)
    for name, amount, unit in parsed_ingredients:
        if amount is None:
            continue
        result[(name, unit)] += amount * multiplier
    return result


def format_ingredient_summary(combined: Dict[Tuple[str, str], float]) -> List[str]:
    """
    結合された材料辞書を表示用文字列リストに変換

    Args:
        combined: 結合された材料辞書

    Returns:
        List[str]: フォーマット済み材料リスト
    """
    output = []
    prefix_units = ["大さじ", "小さじ"]  # 単位が前に来るもの

    for (name, unit), amount in sorted(combined.items()):
        amount_str = str(round(amount, 2))
        if unit in prefix_units:
            formatted = f"{name} {unit}{amount_str}"
        else:
            formatted = f"{name} {amount_str}{unit}"
        output.append(formatted)

    return output

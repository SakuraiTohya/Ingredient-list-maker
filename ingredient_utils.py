import re
from fractions import Fraction
from collections import defaultdict

def convert_mixed_number(s):
    """
    '2と1/2', '1/3', '1.5' などを float に変換。
    """
    s = s.replace('．', '.').replace('・', '/').replace('／', '/').strip()

    # 例: "2と1/2"
    match = re.match(r'(\d+)\s*と\s*(\d+)/(\d+)', s)
    if match:
        whole = int(match.group(1))
        frac = Fraction(int(match.group(2)), int(match.group(3)))
        return float(whole + frac)

    # 例: "1/2"
    match = re.match(r'(\d+)/(\d+)', s)
    if match:
        return float(Fraction(int(match.group(1)), int(match.group(2))))

    # 通常の数字
    try:
        return float(s)
    except:
        return None

def parse_ingredient(item):
    """
    例: '醤油 大さじ1.5' → ('醤油', 1.5, '大さじ')
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
        return str(item).strip(), None, None


def combine_ingredients(parsed_ingredients, multiplier=1.0):
    result = defaultdict(float)
    for name, amount, unit in parsed_ingredients:
        if amount is None:
            continue
        result[(name, unit)] += amount * multiplier
    return result

def format_ingredient_summary(combined):
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

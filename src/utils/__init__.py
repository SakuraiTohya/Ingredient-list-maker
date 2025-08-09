"""
Utils package - ユーティリティ関数群
"""

from .ingredient_utils import parse_ingredient, combine_ingredients, format_ingredient_summary
from .recipe_utils import extract_people_count

# sheet_utilsは動的インポートにして依存関係エラーを回避
__all__ = [
    "parse_ingredient",
    "combine_ingredients", 
    "format_ingredient_summary",
    "extract_people_count"
]

def get_sheet_utils():
    """動的にsheet_utilsをインポート"""
    from .sheet_utils import write_to_spreadsheet
    return write_to_spreadsheet

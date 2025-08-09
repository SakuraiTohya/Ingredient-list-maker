"""
材料ユーティリティのテスト
"""

import pytest
from src.utils.ingredient_utils import parse_ingredient, convert_mixed_number, combine_ingredients


class TestConvertMixedNumber:
    """混合数変換のテスト"""
    
    def test_mixed_number(self):
        """混合数（2と1/2）の変換テスト"""
        assert convert_mixed_number("2と1/2") == 2.5
        assert convert_mixed_number("1と1/4") == 1.25
    
    def test_fraction(self):
        """分数の変換テスト"""
        assert convert_mixed_number("1/2") == 0.5
        assert convert_mixed_number("3/4") == 0.75
    
    def test_decimal(self):
        """小数の変換テスト"""
        assert convert_mixed_number("1.5") == 1.5
        assert convert_mixed_number("2.0") == 2.0
    
    def test_integer(self):
        """整数の変換テスト"""
        assert convert_mixed_number("3") == 3.0
        assert convert_mixed_number("10") == 10.0
    
    def test_invalid_input(self):
        """無効な入力のテスト"""
        assert convert_mixed_number("abc") is None
        assert convert_mixed_number("") is None


class TestParseIngredient:
    """材料解析のテスト"""
    
    def test_basic_parsing(self):
        """基本的な材料解析"""
        name, amount, unit = parse_ingredient("醤油 大さじ2")
        assert name == "醤油"
        assert amount == 2.0
        assert unit == "大さじ"
    
    def test_fraction_parsing(self):
        """分数を含む材料解析"""
        name, amount, unit = parse_ingredient("砂糖 大さじ1/2")
        assert name == "砂糖"
        assert amount == 0.5
        assert unit == "大さじ"
    
    def test_no_amount(self):
        """分量のない材料解析"""
        name, amount, unit = parse_ingredient("塩 適量")
        assert name == "塩 適量"
        assert amount is None
        assert unit == ""


class TestCombineIngredients:
    """材料結合のテスト"""
    
    def test_combine_same_ingredients(self):
        """同じ材料の結合テスト"""
        ingredients = [
            ("醤油", 1.0, "大さじ"),
            ("醤油", 2.0, "大さじ"),
            ("砂糖", 1.0, "小さじ")
        ]
        result = combine_ingredients(ingredients, 1.0)
        assert result[("醤油", "大さじ")] == 3.0
        assert result[("砂糖", "小さじ")] == 1.0
    
    def test_multiplier(self):
        """倍率適用のテスト"""
        ingredients = [("醤油", 1.0, "大さじ")]
        result = combine_ingredients(ingredients, 2.0)
        assert result[("醤油", "大さじ")] == 2.0

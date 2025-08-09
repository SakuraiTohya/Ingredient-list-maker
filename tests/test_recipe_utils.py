"""
レシピユーティリティのテスト
"""

from src.utils.recipe_utils import extract_people_count


class TestExtractPeopleCount:
    """人数抽出機能のテスト"""

    def test_normal_cases(self):
        """通常の人数表記のテスト"""
        assert extract_people_count("2人前") == 2
        assert extract_people_count("4人分") == 4
        assert extract_people_count("1人前") == 1
        assert extract_people_count("10人分") == 10

    def test_edge_cases(self):
        """エッジケースのテスト"""
        assert extract_people_count("") == 1
        assert extract_people_count("適量") == 1
        assert extract_people_count("人数不明") == 1

    def test_complex_patterns(self):
        """複雑なパターンのテスト"""
        assert extract_people_count("約2人前") == 2
        assert extract_people_count("2〜3人前") == 2
        assert extract_people_count("大人2人、子供1人") == 2

    def test_basic_extraction(self):
        """基本的な人数抽出"""
        assert extract_people_count("2人前") == 2
        assert extract_people_count("4人分") == 4
        assert extract_people_count("6個分") == 6

    def test_no_number(self):
        """数字がない場合"""
        assert extract_people_count("適量") == 1
        assert extract_people_count("") == 1
        assert extract_people_count("人前") == 1

    def test_multiple_numbers(self):
        """複数の数字がある場合（最初の数字を取得）"""
        assert extract_people_count("2-3人前") == 2
        assert extract_people_count("約4人分") == 4

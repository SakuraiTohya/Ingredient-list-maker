# マイグレーションガイド

## 古い構造から新しい構造への移行手順

### 1. 現在のファイルのバックアップ
旧ファイルは残したまま、新しい構造での開発を進めます。

### 2. 新しいアプリケーションの実行
```bash
# 新しい構造のアプリを実行
streamlit run app_new.py
```

### 3. テストの実行
```bash
# 開発用依存関係のインストール
pip install -r requirements-dev.txt

# テストの実行
pytest tests/ -v
```

### 4. 動作確認後の移行
新しい構造での動作確認が完了したら：

```bash
# 旧ファイルを削除
rm kurashiru_scraper.py
rm delishkitchen_scraper.py
rm ingredient_utils.py

# 新しいメインアプリに置き換え
mv app_new.py app.py
```

## 主要な変更点

### インポート文の変更
```python
# 旧
from kurashiru_scraper import get_recipe_info_from_kurashiru
from ingredient_utils import parse_ingredient

# 新
from src.scrapers import get_recipe_info_from_kurashiru
from src.utils import parse_ingredient
```

### エラーハンドリングの強化
- タイムアウト設定の追加
- より詳細なエラーメッセージ
- 例外処理の改善

### 型安全性の向上
- 全関数に型ヒントを追加
- mypy による型チェック対応

# プロジェクト構成

## 整理後のディレクトリ構造

```
Ingredient-list-maker/
│
├── src/                          # ソースコード
│   ├── __init__.py              # パッケージ初期化
│   ├── scrapers/                # スクレイピング関連
│   │   ├── __init__.py
│   │   ├── kurashiru_scraper.py
│   │   └── delishkitchen_scraper.py
│   └── utils/                   # ユーティリティ関数
│       ├── __init__.py
│       ├── ingredient_utils.py  # 材料解析・結合
│       ├── recipe_utils.py      # レシピ関連ユーティリティ
│       └── sheet_utils.py       # スプレッドシート操作
│
├── tests/                       # テストコード
│   ├── conftest.py             # テスト設定
│   ├── test_ingredient_utils.py
│   └── test_recipe_utils.py
│
├── config/                      # 設定ファイル
│   └── settings.py             # アプリケーション設定
│
├── docs/                       # ドキュメント
│   └── project_structure.md    # このファイル
│
├── app.py                      # 旧メインアプリ（移行前）
├── app_new.py                  # 新メインアプリ（構造整理後）
├── requirements.txt            # 本番用依存関係
├── requirements-dev.txt        # 開発用依存関係
└── README.md                   # プロジェクト説明
```

## 主な改善点

### 1. モジュール化とコードの分離
- **スクレイピング機能**: `src/scrapers/` に分離
- **ユーティリティ関数**: `src/utils/` に分離
- **設定**: `config/settings.py` に集約

### 2. エラーハンドリングの強化
- 各スクレイパーでのタイムアウト設定
- 詳細なエラーメッセージ
- 例外処理の改善

### 3. 型ヒントの追加
- 全関数に型ヒントを追加
- 可読性と保守性の向上

### 4. テストの追加
- 材料解析機能のユニットテスト
- レシピユーティリティのテスト
- pytest フレームワークの採用

### 5. 開発環境の整備
- 開発用依存関係の分離
- コードフォーマッターの追加（black）
- リンターの追加（flake8）
- 型チェッカーの追加（mypy）

## 使用方法

### 開発環境のセットアップ
```bash
# 開発用依存関係のインストール
pip install -r requirements-dev.txt

# テストの実行
pytest tests/

# コードフォーマット
black src/ tests/

# リント
flake8 src/ tests/

# 型チェック
mypy src/
```

### アプリケーションの実行
```bash
# 新しい構造のアプリを実行
streamlit run app_new.py
```

# 技術仕様書

## 🔧 技術スタックの選定理由

### フロントエンド: Streamlit
- **選定理由**: Pythonのみで完結するWebアプリ開発
- **メリット**: 短期間でのプロトタイプ開発、データサイエンス向け
- **トレードオフ**: カスタマイズ性はReactより劣る

### スクレイピング: BeautifulSoup4 + Requests
- **選定理由**: Pythonエコシステムでの標準的なスクレイピングライブラリ
- **メリット**: 軽量、学習コストが低い
- **代替案検討**: Selenium（重い）、Scrapy（オーバースペック）

### データ処理: 正規表現 + 型ヒント
- **選定理由**: 材料の分量解析に最適
- **工夫点**: 分数・混合数対応、型安全性の確保

## 📊 パフォーマンス考慮事項

### スクレイピング最適化
```python
# タイムアウト設定による応答性向上
requests.get(url, timeout=10)

# 効率的なHTML解析
soup.select("ul.ingredient-list li.ingredient")  # CSS セレクター使用
```

### メモリ使用量削減
- ジェネレーター使用による大量データ処理
- 不要なデータの早期解放

## 🛡️ セキュリティ対策

### スクレイピング
- User-Agentの設定によるブロック回避
- レート制限の考慮（将来的に実装予定）

### API連携
- Google Service Account認証
- 秘匿情報のStreamlit Secrets管理

## 📈 スケーラビリティ

### 新サイト対応
```python
# プラガブルなスクレイパー設計
class BaseScraper:
    def get_recipe_info(self, url: str) -> Optional[Dict]:
        raise NotImplementedError
```

### 国際化対応
- 分量解析の多言語対応余地
- 設定ファイルによる言語切り替え

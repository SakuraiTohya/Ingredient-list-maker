# 🛒 Ingredient List Maker for Recipes

**複数のレシピサイトから材料を自動抽出し、買い物リストを生成するWebアプリケーション**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

このアプリは、**クラシル（kurashiru）とデリッシュキッチン（delish kitchen）**のレシピURLから材料情報を自動的に抽出し、複数人分の材料を合算して買い物リストを生成します。生成されたリストは**Googleスプレッドシートに自動出力**することも可能です。

## 🚀 ライブデモ  
📍[アプリを試してみる](https://ingredient-list-maker-dj2ly2z54u7u3wquznrcih.streamlit.app/)

## 🎯 プロジェクトの特徴

- **モジュラー設計**: 機能ごとに分離された保守しやすいコード構造
- **型安全性**: TypeScript風の型ヒントによる堅牢な実装
- **テスト駆動開発**: pytestによる包括的なユニットテスト
- **CI/CD対応**: 自動化されたテストとデプロイメント準備完了

---

## ✨ 主な機能

- 複数のレシピURLをまとめて入力可能  
- 各レシピごとに「作りたい人数」を設定  
- 材料を**人数に応じて自動的に合算**  
- 「適量」「少々」など分量不明な材料を別枠で表示  
- **スプレッドシートへの出力ON/OFF切り替え可能**  
- **材料名や分量を手動で編集可能**（カスタマイズ自由）

---

## 🛠 使い方

1. クラシルまたはデリッシュキッチンのレシピURLを入力  
2. 各レシピに対して「作りたい人数」を入力  
    - ※「○個分」などのレシピには非対応です  
3. 出力先のGoogleスプレッドシートのURLを入力  
    - ※自分が**編集権限を持つスプレッドシート**にしてください  
4. 必要に応じて「材料名」や「分量」の変更を行う  
5. 「✅ 買い物リストを作成」ボタンをクリック  
6. 結果が画面に表示され、**指定があればスプレッドシートにも自動で反映されます**

---

## 📦 使用技術

- **Frontend**: [Streamlit](https://streamlit.io/) - モダンなWebアプリフレームワーク
- **Scraping**: [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) + [Requests](https://requests.readthedocs.io/) - 効率的なWebスクレイピング
- **API Integration**: [gspread](https://github.com/burnash/gspread) + Google Sheets API - クラウドデータ連携
- **Testing**: [pytest](https://pytest.org/) - 包括的なユニットテスト
- **Code Quality**: [black](https://black.readthedocs.io/), [flake8](https://flake8.pycqa.org/), [mypy](https://mypy.readthedocs.io/) - コード品質管理

## 🏗️ アーキテクチャ

```
src/
├── scrapers/     # レシピサイト別スクレイピング機能
├── utils/        # 共通ユーティリティ（材料解析、スプレッドシート操作）
tests/            # 包括的なユニットテスト
config/           # アプリケーション設定
docs/             # 技術文書・API仕様
```

詳細は [アーキテクチャ文書](docs/architecture.md) をご覧ください。

---

## 🔐 環境変数（Streamlit Secrets）

以下の形式で、Googleサービスアカウントの`credentials.json`を**Streamlit Secrets**に登録してください：

```toml
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "your-service@your-project.iam.gserviceaccount.com"
client_id = "..."
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/..."

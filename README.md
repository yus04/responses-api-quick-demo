# responses-api-quick-demo

Azure OpenAI の **Responses API** を使い、5 つのツールの中からモデルが適切なものを自動選択するクイックデモです。

---

## 概要

`demo.py` は以下の 5 つのツールを定義し、サンプル文章ごとにどのツールがどのパラメーターとともに呼ばれるかを Responses API で確認できます。

| # | ツール名 | 説明 |
|---|----------|------|
| 1 | `get_weather` | 指定都市の天気情報（天気・気温・湿度）を取得する |
| 2 | `search_web` | キーワードでウェブ検索を行い結果を返す |
| 3 | `send_email` | 指定した宛先へメールを送信する |
| 4 | `calculate` | 数式を評価して計算結果を返す |
| 5 | `translate_text` | テキストを指定した言語に翻訳する |

---

## 前提条件

- [uv](https://docs.astral.sh/uv/) 0.4 以上
- [Azure CLI](https://learn.microsoft.com/ja-jp/cli/azure/install-azure-cli) (`az`) インストール済み
- Azure OpenAI リソース（Responses API 対応のデプロイ）
- Azure OpenAI リソースに対して **`Cognitive Services OpenAI User`** 以上のロールが付与されたアカウント

> **API Key 認証は使用しません。** 管理者ポリシーにより API Key が無効化されているため、Entra ID (DefaultAzureCredential) で認証します。

> Python インタープリターは uv が自動的に管理するため、別途インストール不要です。

---

## セットアップ

### 1. Azure CLI でログイン

```bash
az login
```

ブラウザが開き、Entra ID (Azure AD) への認証を求められます。
ブラウザが使えない環境（SSH 等）では以下のデバイスコードフローを使用してください。

```bash
az login --use-device-code
```

ログイン後、対象サブスクリプションをアクティブにします。

```bash
# サブスクリプション一覧を確認
az account list --output table

# 使用するサブスクリプションを設定
az account set --subscription "<サブスクリプション名または ID>"
```

### 2. Azure OpenAI リソースへのロール付与（初回のみ・管理者が実施）

デモを実行するユーザーに以下のロールを付与してもらう必要があります。

```bash
# 例: ユーザー saitoyu@example.com に Cognitive Services OpenAI User を付与
az role assignment create \
  --role "Cognitive Services OpenAI User" \
  --assignee "saitoyu@example.com" \
  --scope "/subscriptions/<サブスクリプション ID>/resourceGroups/<リソースグループ>/providers/Microsoft.CognitiveServices/accounts/<リソース名>"
```

> ロールの反映には数分かかる場合があります。

### 3. 依存関係をインストール

```bash
uv sync
```

`uv sync` は `.venv` 仮想環境の作成・依存パッケージのインストールを一括で行います。
`azure-identity` パッケージも自動的にインストールされます。

### 4. 環境変数の設定

`.env.example` をコピーして `.env` を作成し、値を入力してください。

```bash
cp .env.example .env
```

| 環境変数 | 必須 | 説明 |
|----------|------|------|
| `AZURE_OPENAI_ENDPOINT` | ✅ | Azure OpenAI のエンドポイント URL |
| `AZURE_OPENAI_DEPLOYMENT` | ― | デプロイ名（省略時: `gpt-4o`） |

> `AZURE_OPENAI_API_KEY` は**不要**です。Entra ID トークンで認証するため設定しないでください。

`.env` ファイルが存在する場合、スクリプト起動時に自動で読み込まれます。
シェルで既に環境変数が設定されている場合はそちらが優先されます。

---

## 実行方法

```bash
uv run demo.py
```

`uv run` は `.venv` 内の Python を使って自動的にスクリプトを実行します。
仮想環境の有効化（`source .venv/bin/activate`）は不要です。

---

## 実行例

```
============================================================
Azure OpenAI Responses API - Tool Selection Demo
============================================================
モデル: gpt-4o

[サンプル 1]
入力: 東京の今日の天気を教えてください。
  ツール名  : get_weather
  パラメーター: {
    "city": "東京",
    "unit": "celsius"
}

[サンプル 2]
入力: Python の最新バージョンについて調べてください。
  ツール名  : search_web
  パラメーター: {
    "query": "Python 最新バージョン",
    "num_results": 5
}

[サンプル 3]
入力: 田中さん（tanaka@example.com）に明日の10時からの会議について連絡メールを送ってください。
  ツール名  : send_email
  パラメーター: {
    "to": "tanaka@example.com",
    "subject": "明日の会議について",
    "body": "田中さん、\n\n明日の10時から会議があります。よろしくお願いいたします。"
}

[サンプル 4]
入力: 123 × 456 はいくつですか？
  ツール名  : calculate
  パラメーター: {
    "expression": "123 * 456"
}

[サンプル 5]
入力: 「ありがとうございます」を英語とフランス語に翻訳してください。
  ツール名  : translate_text
  パラメーター: {
    "text": "ありがとうございます",
    "target_language": "English"
}
============================================================
デモ完了
============================================================
```

---

## ツールを選ばせるサンプル文章の例

各ツールに対応するサンプル文章の例を示します。

### `get_weather` — 天気取得

```
東京の今日の天気を教えてください。
大阪の明日の気温は何度ですか？
New York の今の天気を摂氏で教えてください。
```

### `search_web` — ウェブ検索

```
Python の最新バージョンについて調べてください。
Azure OpenAI の料金プランを検索してください。
最近の AI ニュースを 10 件取得してください。
```

### `send_email` — メール送信

```
田中さん（tanaka@example.com）に明日の10時からの会議について連絡メールを送ってください。
上司（boss@company.com）に今週のレポートを送付してください。
```

### `calculate` — 計算

```
123 × 456 はいくつですか？
(10 + 5) ÷ 3 を計算してください。
2 の 10 乗はいくらですか？
```

### `translate_text` — 翻訳

```
「ありがとうございます」を英語とフランス語に翻訳してください。
"Hello, World!" を日本語に翻訳してください。
"Bonjour" はどういう意味ですか？日本語に訳してください。
```

---

## ファイル構成

```
responses-api-quick-demo/
├── demo.py           # メインスクリプト
├── pyproject.toml    # プロジェクト設定・依存ライブラリ定義 (uv)
├── uv.lock           # ロックファイル（再現性のある依存解決）
├── .env.example      # 環境変数のテンプレート（API Key なし）
└── README.md         # このファイル
```

---

## 認証の仕組み

このデモは `azure-identity` の `DefaultAzureCredential` を使用します。
以下の順番で認証情報を自動的に探索します。

| 優先順位 | 認証方法 | 使用場面 |
|---------|----------|----------|
| 1 | 環境変数 (`AZURE_CLIENT_ID` 等) | CI/CD・サービスプリンシパル |
| 2 | Managed Identity | Azure 上のVMやコンテナー |
| 3 | Azure CLI (`az login`) | ローカル開発 |
| 4 | Azure Developer CLI (`azd auth login`) | ローカル開発 (azd) |

ローカル開発では **`az login`** が最も手軽です。

---

## 依存ライブラリの管理

```bash
# パッケージの追加
uv add <package>

# パッケージの削除
uv remove <package>

# ロックファイルを元に環境を再現
uv sync

# 依存関係の一覧表示
uv pip list
```

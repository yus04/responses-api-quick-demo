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

- Python 3.9 以上
- Azure OpenAI リソース（Responses API 対応のデプロイ）

---

## セットアップ

### 1. 依存ライブラリのインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

| 環境変数 | 必須 | 説明 |
|----------|------|------|
| `AZURE_OPENAI_ENDPOINT` | ✅ | Azure OpenAI のエンドポイント URL（例: `https://<your-resource>.openai.azure.com/`） |
| `AZURE_OPENAI_API_KEY` | ✅ | Azure OpenAI の API キー |
| `AZURE_OPENAI_DEPLOYMENT` | ― | デプロイ名（省略時: `gpt-4o`） |

**Linux / macOS:**

```bash
export AZURE_OPENAI_ENDPOINT="https://<your-resource>.openai.azure.com/"
export AZURE_OPENAI_API_KEY="<your-api-key>"
export AZURE_OPENAI_DEPLOYMENT="gpt-4o"
```

**Windows (PowerShell):**

```powershell
$env:AZURE_OPENAI_ENDPOINT = "https://<your-resource>.openai.azure.com/"
$env:AZURE_OPENAI_API_KEY  = "<your-api-key>"
$env:AZURE_OPENAI_DEPLOYMENT = "gpt-4o"
```

---

## 実行方法

```bash
python demo.py
```

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
├── requirements.txt  # Python 依存ライブラリ
└── README.md         # このファイル
```

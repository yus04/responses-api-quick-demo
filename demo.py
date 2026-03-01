#!/usr/bin/env python3
"""
Azure OpenAI Responses API Quick Demo - Tool Selection

このスクリプトは、Azure OpenAI の Responses API を使って
5 つのツールの中から適切なものをモデルが選択する様子を示します。

必要な環境変数:
  AZURE_OPENAI_ENDPOINT   - Azure OpenAI のエンドポイント URL
  AZURE_OPENAI_API_KEY    - Azure OpenAI の API キー
  AZURE_OPENAI_DEPLOYMENT - デプロイ名 (省略時: gpt-4o)
"""

import json
import os
import sys

from openai import AzureOpenAI

# ---------------------------------------------------------------------------
# クライアント初期化
# ---------------------------------------------------------------------------

def create_client() -> AzureOpenAI:
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    if not endpoint or not api_key:
        print(
            "エラー: 環境変数 AZURE_OPENAI_ENDPOINT と AZURE_OPENAI_API_KEY を設定してください。",
            file=sys.stderr,
        )
        sys.exit(1)
    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version="2025-03-01-preview",
    )


# ---------------------------------------------------------------------------
# ツール定義 (5 つ)
# ---------------------------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "name": "get_weather",
        "description": (
            "指定した都市の現在の天気情報（天気の状態、気温、湿度）を取得します。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "天気を調べたい都市名（例: 東京、大阪、New York）",
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "気温の単位。省略時は celsius。",
                },
            },
            "required": ["city"],
        },
    },
    {
        "type": "function",
        "name": "search_web",
        "description": (
            "指定したキーワードでウェブ検索を行い、関連する情報を返します。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "検索クエリ文字列",
                },
                "num_results": {
                    "type": "integer",
                    "description": "取得する検索結果の件数（デフォルト: 5）",
                },
            },
            "required": ["query"],
        },
    },
    {
        "type": "function",
        "name": "send_email",
        "description": (
            "指定した宛先にメールを送信します。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "送信先のメールアドレスまたは受信者名",
                },
                "subject": {
                    "type": "string",
                    "description": "メールの件名",
                },
                "body": {
                    "type": "string",
                    "description": "メール本文",
                },
            },
            "required": ["to", "subject", "body"],
        },
    },
    {
        "type": "function",
        "name": "calculate",
        "description": (
            "数式を評価して計算結果を返します。四則演算・べき乗・括弧が使用できます。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "計算したい数式（例: '123 * 456', '(10 + 5) / 3'）",
                },
            },
            "required": ["expression"],
        },
    },
    {
        "type": "function",
        "name": "translate_text",
        "description": (
            "テキストを指定した言語に翻訳します。"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "翻訳するテキスト",
                },
                "target_language": {
                    "type": "string",
                    "description": "翻訳先の言語（例: English, French, 日本語, 中文）",
                },
                "source_language": {
                    "type": "string",
                    "description": "翻訳元の言語。省略時は自動検出。",
                },
            },
            "required": ["text", "target_language"],
        },
    },
]

# ---------------------------------------------------------------------------
# サンプル文章
# ---------------------------------------------------------------------------

SAMPLES = [
    "東京の今日の天気を教えてください。",
    "Python の最新バージョンについて調べてください。",
    "田中さん（tanaka@example.com）に明日の10時からの会議について連絡メールを送ってください。",
    "123 × 456 はいくつですか？",
    "「ありがとうございます」を英語とフランス語に翻訳してください。",
]

# ---------------------------------------------------------------------------
# メイン処理
# ---------------------------------------------------------------------------

def run_demo(client: AzureOpenAI, deployment: str) -> None:
    print("=" * 60)
    print("Azure OpenAI Responses API - Tool Selection Demo")
    print("=" * 60)
    print(f"モデル: {deployment}\n")

    for i, sample in enumerate(SAMPLES, start=1):
        print(f"[サンプル {i}]")
        print(f"入力: {sample}")

        response = client.responses.create(
            model=deployment,
            input=sample,
            tools=TOOLS,
        )

        tool_calls_found = False
        for item in response.output:
            if item.type == "function_call":
                tool_calls_found = True
                args = json.loads(item.arguments) if isinstance(item.arguments, str) else item.arguments
                print(f"  ツール名  : {item.name}")
                print(f"  パラメーター: {json.dumps(args, ensure_ascii=False, indent=4)}")

        if not tool_calls_found:
            # ツールが選ばれなかった場合はテキスト応答を表示
            for item in response.output:
                if hasattr(item, "content"):
                    for content in item.content:
                        if hasattr(content, "text"):
                            print(f"  テキスト応答: {content.text}")

        print()

    print("=" * 60)
    print("デモ完了")
    print("=" * 60)


if __name__ == "__main__":
    client = create_client()
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    run_demo(client, deployment)

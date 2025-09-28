# NOTE_AUTOPOST_SCRIPT

Note と Twitter の連携を自動化するためのサンプルスクリプトです。恋愛・人間関係を男性視点でリアルに語りつつ、日常の感情や生活改善、AI 活用を織り交ぜたコンテンツ戦略をそのまま反映させています。

## 機能概要

- Note への投稿本文（無料パート＋有料パート）と価格帯（300〜500 円）を自動生成
- Note 公開後に Twitter へシェア投稿（この投稿は 1 日 4 回の定常投稿とは別枠）
- 1 日 4 回、テーマをローテーションしながら定常ツイートを作成
- 環境変数で Note / Twitter の認証情報と投稿時刻、タイムゾーンを設定可能

> **重要**: 実際の Note への投稿や Twitter API 呼び出しはダミー実装になっています。`NoteClient`/`TwitterClient` の中身を本番環境用に差し替えて利用してください。

## 必要な環境変数

| 変数名 | 説明 |
| --- | --- |
| `NOTE_EMAIL` | Note ログイン用メールアドレス |
| `NOTE_PASSWORD` | Note ログイン用パスワード |
| `NOTE_PRICE_MIN` | 有料部分の最低価格（デフォルト 300） |
| `NOTE_PRICE_MAX` | 有料部分の最高価格（デフォルト 500） |
| `TWITTER_API_KEY` | Twitter API Key |
| `TWITTER_API_SECRET` | Twitter API Secret |
| `TWITTER_ACCESS_TOKEN` | Twitter Access Token |
| `TWITTER_ACCESS_TOKEN_SECRET` | Twitter Access Token Secret |
| `TWITTER_POST_TIMES` | カンマ区切りの HH:MM リスト（例: `08:30,12:30,18:30,22:30`） |
| `APP_TIMEZONE` | IANA タイムゾーン名（デフォルト `Asia/Tokyo`） |

## 使い方

```bash
export NOTE_EMAIL="your@mail.com"
export NOTE_PASSWORD="your-password"
export TWITTER_API_KEY="..."
export TWITTER_API_SECRET="..."
export TWITTER_ACCESS_TOKEN="..."
export TWITTER_ACCESS_TOKEN_SECRET="..."

python -m note_auto.app
```

実行すると 1 日分の Note 記事とツイートが生成され、ログに結果が出力されます。

## カスタマイズ

- テーマやトークポイントを増やしたい場合は `note_auto/content_plan.py` 内の `THEMES` を編集してください。
- 実際に投稿処理を行う場合は `note_client.py` と `twitter_client.py` のダミー実装を API 呼び出しに置き換えます。
- 定常ツイートの配信時刻を変更したい場合は `TWITTER_POST_TIMES` を調整してください（Note シェア投稿は別枠扱いで、ランダムな数分後に送信されます）。

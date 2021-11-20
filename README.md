# notion-api-tools
Notionに後で読む記事を登録する

## 事前準備
- NotionのAPI Tokenを取得
- Notionに記事登録用のデータベースのIDを取得

## 使い方
```bash
# ビルド
docker build -t notion \                                          
--build-arg NOTION_TOKEN="NotionのAPI Token" \
--build-arg NOTION_DATABASE_ID="記事登録用データベースID" .

# 実行
docker run --rm -i -t notion python post_db.py https://developers.notion.com/reference/intro
```

## APIキーの取得方法
- [My integrations](https://www.notion.so/my-integrations)にアクセス
- `New Integration`をクリック
- キーの名前を決めてSumbit
- `SECRET`を取得
- 

## 記事登録用のデータベースのIDを取得
- 右上の`･･･`から`copy link to view`をクリック
- 取得したlinkから、`https://www.notion.so/`と`?`の間の文字列（＝データベースID）を取得
  - `https://www.notion.so/xxxxxxxxxxxxxxxxxxxx?v=yyyyyyyyyyyyyyyyyyyyyyyy`なら`xxxxxxxxxxxxxxxxxxxx`の部分

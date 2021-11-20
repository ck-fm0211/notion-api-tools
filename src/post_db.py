import json
import argparse
import requests
import lxml.html
import os
import validators


NOTION_API_URL = 'https://api.notion.com/v1/pages'

def _get_page_info(target_url):
    """
    ページのタイトルを取得する
    """

    # Webページ取得
    response = requests.get(target_url)
    # スクレイピング
    html = lxml.html.fromstring(response.content)

    # ページタイトルを取得
    try:
        page_title = html.xpath("//title/text()")[0]
    except IndexError as e:
        # タイトルが取得できなかった場合、URL文字列をそのまま表示する
        page_title = target_url

    return page_title

def post_content(url, page_title, token, database_id):

    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json',
        'Notion-Version': '2021-05-13',
    }

    data = json.dumps(
        {
        "parent": { "database_id": database_id},
        "properties": {
                "Name": {
                    "title": [
                        {"text":
                            {
                                "content": page_title
                                ,"link": {
                                    "url": url
                                }
                            }
                        }
                    ]
            },
            "URL": {
                    "url": url
                }
            }
        }
    )
    try:
        response = requests.post(NOTION_API_URL, headers=headers, data=data)
    except requests.exceptions.RequestException as e:
        print("エラー : ",e)
    else:
        print(response)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Notionに後で読む記事を登録する')

    # 3. parser.add_argumentで受け取る引数を追加していく
    parser.add_argument('url', help='NotionのDBにinsertしたいURL')
    parser.add_argument('-t', '--token', help='Notionに登録するためのTOKEN')
    parser.add_argument('-db', '--database', help='登録先のデータベースID')

    args = parser.parse_args()

    token = os.getenv('NOTION_TOKEN', args.token)
    database_id = os.getenv('NOTION_DATABASE_ID', args.database)

    if token is None:
        print('環境変数`NOTION_TOKEN`またはコマンド引数`-t/--token`にNotionに登録するためのTOKENを設定してください。')
        exit(1)

    if database_id is None:
        print('環境変数`NOTION_DATABASE_ID`またはコマンド引数`-db/--database`に登録先のデータベースIDを設定してください。')
        exit(1)

    if not validators.url(args.url):
        print(f"{args.url}は有効なURLではありません")
        exit(1)

    page_title = _get_page_info(args.url)

    post_content(args.url, page_title, token, database_id)

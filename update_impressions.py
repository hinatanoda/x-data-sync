import os
import json
import requests
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 1. GitHub SecretsからGOOGLE_API_CREDENTIALS（Google Sheets APIの認証情報）を取得
google_credentials_json = os.getenv('GOOGLE_API_CREDENTIALS')

# 2. JSON文字列を辞書に変換
google_credentials = json.loads(google_credentials_json)

# 3. Google Sheets APIにアクセスするための認証情報を設定
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    google_credentials,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

# 4. X APIからインプレッション数を取得
X_BEARER_TOKEN = os.getenv('X_BEARER_TOKEN')
USER_ID = 'your_user_id'  # あなたのXアカウントIDに置き換えてください
url = f'https://api.twitter.com/2/users/{USER_ID}/tweets'

headers = {
    'Authorization': f'Bearer {X_BEARER_TOKEN}',
}

params = {
    'max_results': 5,  # 最新5件のツイートを取得（任意の件数に変更可）
}

response = requests.get(url, headers=headers, params=params)
data = response.json()

# インプレッション数の取得（仮に最後のツイートのインプレッション数を取得）
impressions = 0
for tweet in data.get('data', []):
    tweet_id = tweet['id']
    tweet_url = f'https://api.twitter.com/2/tweets/{tweet_id}'
    tweet_response = requests.get(tweet_url, headers=headers)
    tweet_data = tweet_response.json()
    impressions += tweet_data.get('data', {}).get('public_metrics', {}).get('impression_count', 0)

# 5. GitHub SecretsからスプレッドシートIDを取得
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')  # GitHub Secretsに保存されたスプレッドシートIDを取得
RANGE_NAME = 'X分析シート!A1'  # データを入力するセル範囲に合わせてください

# 今日の日付を取得
today_date = datetime.now().strftime('%Y-%m-%d')

# 6. インプレッションデータを設定
data_to_update = {
    'values': [
        ['Date', 'Impressions'],
        [today_date, impressions],  # 今日の日付とインプレッション数をセット
    ]
}

# 7. Google Sheets APIを使ってスプレッドシートにデータを更新するリクエストを送る
url = f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{RANGE_NAME}?valueInputOption=RAW'
headers = {
    'Authorization': f'Bearer {credentials.get_access_token().access_token}',
    'Content-Type': 'application/json'
}

# 8. リクエストを送信して、結果を確認
response = requests.put(url, headers=headers, json=data_to_update)

# 9. レスポンスを確認して、更新が成功したか確認
if response.status_code == 200:
    print("Data updated successfully!")
else:
    print(f"Error updating data: {response.status_code} - {response.text}")

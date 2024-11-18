import tweepy
import gspread
from google.oauth2.service_account import Credentials
import os
import json
from datetime import datetime

# 環境変数からGoogle Sheetsの認証情報を取得
google_credentials = json.loads(os.getenv('GOOGLE_API_CREDENTIALS'))  # JSON文字列を辞書に変換

# 認証情報を使ってGoogle Sheets APIにアクセス
credentials = Credentials.from_service_account_info(google_credentials, scopes=['https://www.googleapis.com/auth/spreadsheets'])

# X APIの認証情報（Bearer Token）
BEARER_TOKEN = os.getenv('BEARER_TOKEN')  # GitHub Secretsから取得

# Google Sheets APIの認証情報
SHEET_ID = os.getenv('GOOGLE_SHEET_ID')  # GitHub Secretsから取得

# X APIクライアントの設定
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Google Sheetsの認証設定
client_gspread = gspread.authorize(credentials)

# Googleスプレッドシートの取得
sheet = client_gspread.open_by_key(SHEET_ID).sheet1  # 1番目のシートを選択

# ユーザー名からuser_idを取得
username = 'waav_king'  # 自分のXアカウントのユーザー名
response = client.get_user(username=username)  # ユーザー情報を取得

# 正しいuser_idを取得
user_id = response.data.id  # data属性内にidが含まれています

print(f'User ID: {user_id}')  # 取得したuser_idを表示

# Xのアカウント情報を使ってインプレッション数を取得
tweets = client.get_users_tweets(user_id, tweet_fields=["public_metrics", "text"])

# 現在の日付を取得
today_date = datetime.now().strftime('%Y-%m-%d')

# スプレッドシートに日付列を追加
header_row = sheet.row_values(1)  # 最初の行（ヘッダー行）を取得
if today_date not in header_row:
    sheet.update_cell(1, len(header_row) + 1, today_date)  # 新しい列を追加

# 最も最近のツイートのインプレッション数を取得
if tweets.data is not None:
    for tweet in tweets.data:
        tweet_text = tweet.text
        impressions = tweet.public_metrics['impression_count']

        # 投稿本文を既存データから探すか、新規追加
        all_rows = sheet.get_all_values()
        found = False
        for row_index, row in enumerate(all_rows[1:], start=2):  # 2行目以降を走査
            if row[0] == tweet_text:  # 投稿本文が一致
                found = True
                sheet.update_cell(row_index, len(header_row) + 1, impressions)  # 対応する行にインプレッション数を更新
                break

        # 新規ツイートの場合、最終行に追加
        if not found:
            new_row = [tweet_text] + [''] * (len(header_row) - 1) + [impressions]
            sheet.append_row(new_row)
else:
    print("No tweets found or error in API response.")

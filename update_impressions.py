import tweepy
import gspread
from google.oauth2.service_account import Credentials  # oauth2clientからgoogle.oauth2に変更
import os
import json

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

# Xのアカウント情報を使ってインプレッション数を取得
username = 'waav_king'  # 自分のXアカウントのユーザー名
user = client.get_user(username=username)  # ユーザー情報を取得
user_id = user.id  # 正しいuser_idを取得

# Xのアカウント情報を使ってインプレッション数を取得
tweets = client.get_users_tweets(user_id, tweet_fields=["public_metrics"])

# レスポンスを確認
print(f"API Response: {tweets}")

# 最も最近のツイートのインプレッション数を取得
if tweets.data is not None:
    for tweet in tweets.data:
        impressions = tweet.public_metrics['impression_count']
        # Googleスプレッドシートにインプレッション数を反映
        sheet.append_row([tweet.id, impressions])
else:
    print("No tweets found or error in API response.")

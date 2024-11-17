import tweepy
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# X APIの認証情報（Bearer Token）
BEARER_TOKEN = os.getenv('BEARER_TOKEN')  # GitHub Secretsから取得

# Google Sheets APIの認証情報
GOOGLE_API_CREDENTIALS = os.getenv('GOOGLE_API_CREDENTIALS')  # GitHub Secretsから取得
SHEET_ID = os.getenv('GOOGLE_SHEET_ID')  # GitHub Secretsから取得

# X APIクライアントの設定
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Google Sheetsの認証設定
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    GOOGLE_API_CREDENTIALS, scope)
client_gspread = gspread.authorize(credentials)

# Googleスプレッドシートの取得
sheet = client_gspread.open_by_key(SHEET_ID).sheet1  # 1番目のシートを選択

# Xのアカウント情報を使ってインプレッション数を取得
user_id = '1842515820163043328'  # 自分のXアカウントのIDを設定
tweets = client.get_users_tweets(user_id, tweet_fields=["public_metrics"])

# 最も最近のツイートのインプレッション数を取得
for tweet in tweets.data:
    impressions = tweet.public_metrics['impression_count']
    # Googleスプレッドシートにインプレッション数を反映
    sheet.append_row([tweet.id, impressions])

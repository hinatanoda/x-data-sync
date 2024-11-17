import requests
import json
from oauth2client.service_account import ServiceAccountCredentials
import os

# 環境変数からGoogle Sheetsの認証情報を取得
google_credentials = json.loads(os.getenv('GOOGLE_API_CREDENTIALS'))

# 認証情報を使ってGoogle Sheets APIにアクセス
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    google_credentials,
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

# --- X API情報 ---
BEARER_TOKEN = "YOUR_BEARER_TOKEN"  # XのAPIキー（Bearer Token）をここに入れます
USER_ID = "YOUR_USER_ID"  # XのユーザーIDをここに入れます

def get_impression_count():
    """X APIからインプレッション数を取得"""
    url = f"https://api.twitter.com/2/users/{USER_ID}/tweets"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    
    data = response.json()
    impressions = sum(tweet["public_metrics"]["impression_count"] for tweet in data["data"])
    return impressions

if __name__ == "__main__":
    # インプレッション数を取得して表示（動作確認用）
    impressions = get_impression_count()
    print(f"Today's Impressions: {impressions}")
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

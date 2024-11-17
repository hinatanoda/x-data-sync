import tweepy

# Bearer Tokenを使って認証
BEARER_TOKEN = "your_bearer_token"
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# 自分のユーザーIDを取得
user = client.get_me()
print(user.data.id)  # これがuser_id

import requests

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

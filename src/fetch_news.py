import feedparser, requests, os
from datetime import datetime

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

FEEDS = {
    "デザイン": [
        "https://www.advertimes.com/feed/",
        "https://ascii.jp/rss.xml",
        "https://designassociation.jp/feed/",
        "https://note.com/hashtag/デザイン?format=rss",
        "https://www.cinra.net/feed/",
    ],
    "ファッション": [
        "https://www.fashionsnap.com/feed/",
        "https://www.vogue.co.jp/feed/rss",
        "https://jp.fashionnetwork.com/rss/news.xml",
        "https://hypebeast.com/jp/feed",
        "https://www.elle.com/jp/rss/all.xml/",
    ],
    "政治経済": [
        "https://www3.nhk.or.jp/rss/news/cat4.xml",
        "https://www3.nhk.or.jp/rss/news/cat6.xml",
        "https://toyokeizai.net/list/feed/rss",
        "https://www.nhk.or.jp/rss/news/cat5.xml",
        "https://feeds.feedburner.com/businessinsider-japan",
    ],
    "AI関連": [
        "https://ai-scholar.tech/feed",
        "https://ledge.ai/feed/",
        "https://ainow.ai/feed/",
        "https://www.itmedia.co.jp/aiplus/rss/2.0/index.rdf",
        "https://gigazine.net/news/rss_2.0/",
    ],
}

ICONS = {"デザイン": "🎨", "ファッション": "👗", "政治経済": "📊", "AI関連": "🤖"}

# 会員限定・有料記事を除外するキーワード
BLOCK_KEYWORDS = [
    "会員限定", "有料", "プレミアム", "登録が必要",
    "サブスクリプション", "購読", "ログインが必要"
]

def is_free_article(title, summary=""):
    text = title + summary
    return not any(kw in text for kw in BLOCK_KEYWORDS)

def fetch_category(category, feed_urls):
    articles = []
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:  # 各フィードから最大5件チェックして無料記事を探す
                title = entry.get("title", "（タイトルなし）")
                summary = entry.get("summary", "")
                link = entry.get("link", "")
                if is_free_article(title, summary):
                    articles.append({"title": title, "link": link})
                    break  # 1フィードから1本取得できたら次へ
        except Exception as e:
            print(f"RSS取得エラー ({url}): {e}")
    return articles

def build_message(all_articles):
    today = datetime.now().strftime("%Y年%m月%d日（%a）")
    total = sum(len(v) for v in all_articles.values())
    blocks = [
        {"type": "header", "text": {
            "type": "plain_text",
            "text": f"📰 今日のニュース｜{today}（計{total}本）"
        }},
        {"type": "divider"}
    ]
    for category, articles in all_articles.items():
        icon = ICONS[category]
        lines = [f"*{icon} {category}*"]
        for i, a in enumerate(articles, 1):
            lines.append(f"{i}. {a['title']}")
            if a['link']:
                lines.append(f"   🔗 {a['link']}")
        blocks.append({"type": "section",
                       "text": {"type": "mrkdwn",
                                "text": "\n".join(lines)}})
        blocks.append({"type": "divider"})
    return {"blocks": blocks}

def post_to_slack(payload):
    res = requests.post(SLACK_WEBHOOK_URL, json=payload)
    res.raise_for_status()
    print("Slack投稿完了！")

if __name__ == "__main__":
    all_articles = {}
    for category, urls in FEEDS.items():
        articles = fetch_category(category, urls)
        all_articles[category] = articles
        print(f"{category}: {len(articles)}本取得")
    payload = build_message(all_articles)
    post_to_slack(payload)

import feedparser, requests, os
from datetime import datetime

SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]

FEEDS = {
    "デザイン": [
        "https://www.designweek.co.uk/feed/",
        "https://www.creativebloq.com/feed",
        "https://www.dezeen.com/feed/",
        "https://www.itsnicethat.com/feed",
        "https://www.awwwards.com/blog/feed/",
    ],
    "ファッション": [
        "https://wwd.com/feed/",
        "https://www.voguebusiness.com/rss",
        "https://www.businessoffashion.com/rss/news.rss",
        "https://jp.fashionnetwork.com/rss/news.xml",
        "https://hypebeast.com/feed",
    ],
    "政治経済": [
        "https://www3.nhk.or.jp/rss/news/cat4.xml",
        "https://feeds.reuters.com/reuters/JPBusinessNews",
        "https://www.bloomberg.co.jp/feeds/bbiz.rss",
        "https://toyokeizai.net/list/feed/rss",
        "https://www3.nhk.or.jp/rss/news/cat6.xml",
    ],
}

ICONS = {"デザイン": "🎨", "ファッション": "👗", "政治経済": "📊"}

def fetch_category(category, feed_urls):
    articles = []
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            if feed.entries:
                entry = feed.entries[0]
                articles.append({
                    "title": entry.get("title", "（タイトルなし）"),
                    "link":  entry.get("link", ""),
                })
        except Exception as e:
            print(f"RSS取得エラー ({url}): {e}")
    return articles

def build_message(all_articles):
    today = datetime.now().strftime("%Y年%m月%d日（%a）")
    blocks = [
        {"type": "header", "text": {
            "type": "plain_text",
            "text": f"📰 今日のニュース｜{today}"
        }},
        {"type": "divider"}
    ]
    for category, articles in all_articles.items():
        icon = ICONS[category]
        l

import random
import json
from datetime import datetime, timedelta


SAMPLE_TEXTS = {
    "Tesla": [
        "Tesla's new Model Y update is absolutely incredible! #Tesla #ElectricCar #EV",
        "Just ordered my first Tesla. The autopilot feature is mind-blowing. #Tesla #Autopilot",
        "Tesla stock crashed 10% today. Investors are worried. #Tesla #TSLA #Stock",
        "Elon Musk tweets again about Tesla. The community is divided. #Tesla #ElonMusk",
        "Tesla Supercharger network is expanding rapidly across India #Tesla #EV #India",
        "Terrible experience at Tesla service center. Waited 3 weeks for a simple fix. #Tesla",
        "Tesla FSD beta is getting better every update. Nearly perfect on highways! #Tesla #FSD",
        "Range anxiety is real. Tesla needs to improve charging speed #Tesla #EV",
        "Tesla Cybertruck finally delivered to customers. Love the design! #Cybertruck #Tesla",
        "Competition is heating up. BYD might surpass Tesla in sales. #Tesla #BYD #EV",
        "Tesla's solar roof is the future of energy. #Tesla #SolarEnergy #GreenTech",
        "Disappointed with Tesla's customer service response time. #Tesla #CustomerService",
        "Tesla Model 3 is the most fun car I've ever driven #Tesla #Model3",
        "Is Tesla overvalued? The PE ratio is astronomical. #Tesla #TSLA #Investing",
        "Tesla's AI Day announcements blew my mind. Dojo supercomputer is next level #Tesla #AI",
    ],
    "default": [
        "This is amazing content! Loving every bit of it. #trending #viral",
        "Not sure how I feel about this. Very mixed opinions. #opinion",
        "Breaking news everyone needs to see! #news #breaking",
        "Great product launch today. Highly recommended! #launch #product",
        "Terrible experience with this brand. Never again. #disappointed",
        "The latest update completely broke everything. #fail #tech",
        "Can't believe how popular this has become #viral #trending",
        "Just discovered this and I'm obsessed #discovery #awesome",
        "Warning: this is completely false information! #fakenews #misinformation",
        "Sharing my honest review after 6 months of use #review #honest",
    ]
}

SAMPLE_AUTHORS = [
    "tech_guru_99", "social_jane", "marketing_pro", "data_wizard",
    "news_daily", "trending_now", "viral_content", "honest_reviewer",
    "market_watch", "community_voice", "insider_info", "daily_digest",
    "analyst_mike", "influencer_sarah", "regular_user42", "expert_opinion",
    "breaking_news", "fact_checker", "digital_nomad", "startup_founder"
]


def generate_sample_posts(keyword: str, platform: str, count: int = 100) -> list:
    texts = SAMPLE_TEXTS.get(keyword, SAMPLE_TEXTS["default"])
    posts = []
    base_date = datetime.utcnow() - timedelta(days=30)

    for i in range(count):
        text_base = random.choice(texts)
        author = random.choice(SAMPLE_AUTHORS)
        followers = random.randint(100, 500000)
        likes = random.randint(0, int(followers * 0.1))
        retweets = random.randint(0, int(likes * 0.3))
        replies = random.randint(0, int(likes * 0.2))
        posted_at = base_date + timedelta(
            hours=random.randint(0, 720),
            minutes=random.randint(0, 59)
        )

        import re
        hashtags = re.findall(r'#(\w+)', text_base)

        posts.append({
            'post_id': f'{platform.lower()}_{i+1:05d}',
            'text': text_base,
            'author': author,
            'author_followers': followers,
            'likes': likes,
            'retweets': retweets,
            'replies': replies,
            'platform': platform,
            'posted_at': posted_at,
            'hashtags': json.dumps(hashtags),
            'url': f'https://{platform.lower()}.com/{author}/status/{i+1}'
        })

    return posts


def collect_from_apify(token: str, keyword: str, platform: str, max_items: int = 100):
    """Collect real data using Apify API."""
    try:
        from apify_client import ApifyClient
        client = ApifyClient(token)

        if platform.upper() == 'X':
            actor_id = "apidojo/tweet-scraper"
            run_input = {
                "searchTerms": [keyword],
                "maxItems": max_items,
                "queryType": "Latest"
            }
        else:
            actor_id = "apidojo/facebook-posts-scraper"
            run_input = {
                "searchTerms": [keyword],
                "maxItems": max_items
            }

        run = client.actor(actor_id).call(run_input=run_input)
        posts = []
        import re, json as _json
        from datetime import datetime

        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            text = item.get('text', item.get('full_text', ''))
            if not text:
                continue
            hashtags = re.findall(r'#(\w+)', text)
            posts.append({
                'post_id': str(item.get('id', '')),
                'text': text,
                'author': item.get('author', item.get('user', {}).get('screen_name', 'unknown')),
                'author_followers': item.get('author_followers_count', item.get('user', {}).get('followers_count', 0)),
                'likes': item.get('likes', item.get('favorite_count', 0)),
                'retweets': item.get('retweets', item.get('retweet_count', 0)),
                'replies': item.get('replies', item.get('reply_count', 0)),
                'platform': platform,
                'posted_at': datetime.utcnow(),
                'hashtags': _json.dumps(hashtags),
                'url': item.get('url', '')
            })

        return posts, len(posts)
    except Exception as e:
        raise Exception(f"Apify collection failed: {str(e)}")

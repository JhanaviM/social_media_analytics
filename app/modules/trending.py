"""
Module 2: Trending Topics Detection
Extracts and ranks hashtags, keywords, and phrases by frequency.
"""
import re
from collections import Counter


STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'was', 'are', 'were', 'be', 'been',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'can', 'that', 'this', 'these', 'those',
    'it', 'its', 'i', 'you', 'he', 'she', 'we', 'they', 'my', 'your',
    'his', 'her', 'our', 'their', 'rt', 'via', 'amp', 'just', 'not', 'so'
}


def detect_trends(posts: list) -> dict:
    hashtag_counter = Counter()
    keyword_counter = Counter()
    mention_counter = Counter()
    daily_counts = {}

    for post in posts:
        text = post['text']

        # Hashtags
        hashtags = re.findall(r'#(\w+)', text)
        for tag in hashtags:
            hashtag_counter[tag.lower()] += 1

        # Mentions
        mentions = re.findall(r'@(\w+)', text)
        for m in mentions:
            mention_counter[m.lower()] += 1

        # Keywords (cleaned words)
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        for word in words:
            if word not in STOPWORDS:
                keyword_counter[word] += 1

        # Daily trend
        date_str = str(post.get('posted_at', ''))[:10]
        if date_str and date_str != 'None':
            daily_counts[date_str] = daily_counts.get(date_str, 0) + 1

    top_hashtags = [{'tag': f'#{tag}', 'count': count}
                    for tag, count in hashtag_counter.most_common(20)]
    top_keywords = [{'word': word, 'count': count}
                    for word, count in keyword_counter.most_common(20)]
    top_mentions = [{'mention': f'@{m}', 'count': count}
                    for m, count in mention_counter.most_common(10)]

    sorted_dates = sorted(daily_counts.items())
    timeline = [{'date': d, 'count': c} for d, c in sorted_dates]

    # Trend score = weighted rank by frequency
    all_tags_ranked = []
    for i, (tag, count) in enumerate(hashtag_counter.most_common(50)):
        trend_score = count * (1 + 1 / (i + 1))
        all_tags_ranked.append({'tag': f'#{tag}', 'count': count, 'trend_score': round(trend_score, 2)})

    return {
        'total_posts': len(posts),
        'unique_hashtags': len(hashtag_counter),
        'unique_keywords': len(keyword_counter),
        'top_hashtags': top_hashtags,
        'top_keywords': top_keywords,
        'top_mentions': top_mentions,
        'timeline': timeline,
        'trending_ranked': all_tags_ranked[:20],
        'wordcloud_data': [{'text': tag, 'weight': count}
                           for tag, count in hashtag_counter.most_common(40)]
    }

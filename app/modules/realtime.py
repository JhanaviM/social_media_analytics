"""
Module 10: Real-Time Monitoring
Tracks keyword frequency, spikes, and sentiment in real-time windows.
"""
from collections import defaultdict
import re


def monitor_keywords(posts: list, keyword: str) -> dict:
    keyword_lower = keyword.lower()
    related_terms = set()
    hourly_mentions = defaultdict(int)
    daily_sentiment = defaultdict(lambda: {'positive': 0, 'negative': 0, 'neutral': 0, 'total': 0})
    alerts = []
    co_occurring = defaultdict(int)

    total_mentions = 0
    for post in posts:
        text = post['text']
        text_lower = text.lower()

        if keyword_lower in text_lower:
            total_mentions += 1

            date_str = str(post.get('posted_at', ''))[:10]
            hour_str = str(post.get('posted_at', ''))
            if len(hour_str) >= 13:
                try:
                    hour = int(hour_str[11:13])
                    hourly_mentions[hour] += 1
                except (ValueError, IndexError):
                    pass

            # Extract co-occurring words
            words = re.findall(r'\b[a-zA-Z]{4,}\b', text_lower)
            for word in words:
                if word != keyword_lower and word not in {'this', 'that', 'with', 'have', 'from', 'they', 'been', 'just', 'will', 'more', 'also'}:
                    co_occurring[word] += 1

        # Daily sentiment
        date_str = str(post.get('posted_at', ''))[:10]
        if date_str and date_str != 'None':
            likes = post.get('likes', 0)
            if likes > 100:
                daily_sentiment[date_str]['positive'] += 1
            elif likes < 5:
                daily_sentiment[date_str]['negative'] += 1
            else:
                daily_sentiment[date_str]['neutral'] += 1
            daily_sentiment[date_str]['total'] += 1

    # Spike detection: find hours with unusually high mentions
    avg_hourly = sum(hourly_mentions.values()) / max(len(hourly_mentions), 1)
    for hour, count in hourly_mentions.items():
        if count > avg_hourly * 2:
            alerts.append({
                'type': 'SPIKE',
                'hour': f'{hour:02d}:00',
                'count': count,
                'message': f'Mention spike at {hour:02d}:00 — {count} mentions (avg: {avg_hourly:.1f})'
            })

    # Related terms from co-occurrence
    related_terms = sorted(co_occurring.items(), key=lambda x: x[1], reverse=True)[:15]

    sorted_dates = sorted(daily_sentiment.keys())

    return {
        'keyword': keyword,
        'total_mentions': total_mentions,
        'mention_rate': round(total_mentions / max(len(posts), 1) * 100, 1),
        'hourly_trend': [
            {'hour': f'{h:02d}:00', 'mentions': hourly_mentions.get(h, 0)}
            for h in range(24)
        ],
        'daily_sentiment': [
            {
                'date': d,
                'positive': daily_sentiment[d]['positive'],
                'negative': daily_sentiment[d]['negative'],
                'neutral': daily_sentiment[d]['neutral'],
                'total': daily_sentiment[d]['total'],
            }
            for d in sorted_dates
        ],
        'co_occurring_terms': [
            {'term': term, 'count': count}
            for term, count in related_terms
        ],
        'alerts': alerts[:10],
        'monitoring_summary': {
            'peak_hour': max(hourly_mentions, key=hourly_mentions.get, default=0),
            'peak_count': max(hourly_mentions.values()) if hourly_mentions else 0,
            'total_alerts': len(alerts),
        }
    }

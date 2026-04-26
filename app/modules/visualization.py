"""
Module 7: Data Visualization
Builds chart data for engagement, reach, and sentiment over time.
"""
from collections import defaultdict


def build_charts(posts: list) -> dict:
    daily_engagement = defaultdict(lambda: {'likes': 0, 'retweets': 0, 'replies': 0, 'posts': 0})
    platform_counts = defaultdict(int)
    hourly_posts = defaultdict(int)
    author_reach = defaultdict(int)
    engagement_dist = {'0-10': 0, '11-100': 0, '101-1000': 0, '1000+': 0}

    for post in posts:
        date_str = str(post.get('posted_at', ''))[:10]
        if date_str and date_str != 'None':
            daily_engagement[date_str]['likes'] += post.get('likes', 0)
            daily_engagement[date_str]['retweets'] += post.get('retweets', 0)
            daily_engagement[date_str]['replies'] += post.get('replies', 0)
            daily_engagement[date_str]['posts'] += 1

        hour_str = str(post.get('posted_at', ''))
        if len(hour_str) >= 13:
            try:
                hour = int(hour_str[11:13])
                hourly_posts[hour] += 1
            except (ValueError, IndexError):
                pass

        platform = post.get('platform', 'Unknown')
        platform_counts[platform] += 1

        author = post.get('author', '')
        if author:
            author_reach[author] += post.get('author_followers', 0)

        total_eng = post.get('likes', 0) + post.get('retweets', 0)
        if total_eng <= 10:
            engagement_dist['0-10'] += 1
        elif total_eng <= 100:
            engagement_dist['11-100'] += 1
        elif total_eng <= 1000:
            engagement_dist['101-1000'] += 1
        else:
            engagement_dist['1000+'] += 1

    sorted_dates = sorted(daily_engagement.keys())

    timeline_data = {
        'labels': sorted_dates,
        'likes': [daily_engagement[d]['likes'] for d in sorted_dates],
        'retweets': [daily_engagement[d]['retweets'] for d in sorted_dates],
        'replies': [daily_engagement[d]['replies'] for d in sorted_dates],
        'posts': [daily_engagement[d]['posts'] for d in sorted_dates],
    }

    hourly_data = {
        'labels': [f'{h:02d}:00' for h in range(24)],
        'counts': [hourly_posts.get(h, 0) for h in range(24)]
    }

    top_reach = sorted(author_reach.items(), key=lambda x: x[1], reverse=True)[:10]

    total_likes = sum(p.get('likes', 0) for p in posts)
    total_retweets = sum(p.get('retweets', 0) for p in posts)
    total_replies = sum(p.get('replies', 0) for p in posts)
    total_reach = sum(p.get('author_followers', 0) for p in posts)
    n = len(posts)

    return {
        'kpis': {
            'total_posts': n,
            'total_likes': total_likes,
            'total_retweets': total_retweets,
            'total_replies': total_replies,
            'total_reach': total_reach,
            'avg_likes': round(total_likes / n, 1) if n else 0,
            'avg_retweets': round(total_retweets / n, 1) if n else 0,
            'engagement_rate': round((total_likes + total_retweets + total_replies) / max(total_reach, 1) * 100, 3),
        },
        'timeline': timeline_data,
        'hourly': hourly_data,
        'platform_breakdown': [
            {'platform': k, 'count': v} for k, v in platform_counts.items()
        ],
        'engagement_distribution': [
            {'range': k, 'count': v} for k, v in engagement_dist.items()
        ],
        'top_reach_authors': [
            {'author': a, 'reach': r} for a, r in top_reach
        ],
    }

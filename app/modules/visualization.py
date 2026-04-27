"""Module 7: Data Visualization — pure Python, no pandas."""
from collections import defaultdict


def build_charts(posts: list) -> dict:
    daily = defaultdict(lambda: {'likes': 0, 'retweets': 0, 'replies': 0, 'posts': 0})
    hourly = defaultdict(int)
    platform_counts = defaultdict(int)
    author_reach = defaultdict(int)
    eng_dist = {'0-10': 0, '11-100': 0, '101-1000': 0, '1000+': 0}
    total_likes = total_retweets = total_replies = total_reach = 0

    for post in posts:
        date_str = str(post.get('posted_at', ''))[:10]
        if date_str and date_str != 'None':
            daily[date_str]['likes']    += post.get('likes', 0)
            daily[date_str]['retweets'] += post.get('retweets', 0)
            daily[date_str]['replies']  += post.get('replies', 0)
            daily[date_str]['posts']    += 1
        ts = str(post.get('posted_at', ''))
        if len(ts) >= 13:
            try:
                hourly[int(ts[11:13])] += 1
            except ValueError:
                pass
        platform_counts[post.get('platform', 'Unknown')] += 1
        author = post.get('author', '')
        if author:
            author_reach[author] += post.get('author_followers', 0)
        eng = post.get('likes', 0) + post.get('retweets', 0)
        if eng <= 10:        eng_dist['0-10']     += 1
        elif eng <= 100:     eng_dist['11-100']   += 1
        elif eng <= 1000:    eng_dist['101-1000'] += 1
        else:                eng_dist['1000+']    += 1
        total_likes    += post.get('likes', 0)
        total_retweets += post.get('retweets', 0)
        total_replies  += post.get('replies', 0)
        total_reach    += post.get('author_followers', 0)

    n = len(posts) or 1
    dates = sorted(daily.keys())
    return {
        'kpis': {
            'total_posts': n, 'total_likes': total_likes,
            'total_retweets': total_retweets, 'total_replies': total_replies,
            'total_reach': total_reach,
            'avg_likes': round(total_likes / n, 1),
            'avg_retweets': round(total_retweets / n, 1),
            'engagement_rate': round((total_likes + total_retweets + total_replies) / max(total_reach, 1) * 100, 3),
        },
        'timeline': {
            'labels': dates,
            'likes':    [daily[d]['likes']    for d in dates],
            'retweets': [daily[d]['retweets'] for d in dates],
            'replies':  [daily[d]['replies']  for d in dates],
            'posts':    [daily[d]['posts']    for d in dates],
        },
        'hourly': {
            'labels': [f'{h:02d}:00' for h in range(24)],
            'counts': [hourly.get(h, 0) for h in range(24)],
        },
        'platform_breakdown': [{'platform': k, 'count': v} for k, v in platform_counts.items()],
        'engagement_distribution': [{'range': k, 'count': v} for k, v in eng_dist.items()],
        'top_reach_authors': [
            {'author': a, 'reach': r}
            for a, r in sorted(author_reach.items(), key=lambda x: x[1], reverse=True)[:10]
        ],
    }

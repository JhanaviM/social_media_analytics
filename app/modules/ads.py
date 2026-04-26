"""
Module 8: Ad Campaign Optimization
Calculates CTR, Conversion Rate, ROI and provides campaign insights.
"""


def optimize_ads(posts: list) -> dict:
    total_impressions = sum(p.get('author_followers', 0) for p in posts)
    total_clicks = sum(p.get('likes', 0) + p.get('retweets', 0) for p in posts)
    total_conversions = int(total_clicks * 0.032)  # Estimated 3.2% conversion
    total_cost = len(posts) * 2.5  # Estimated $2.5 per post promotion
    revenue_per_conversion = 45.0
    total_revenue = total_conversions * revenue_per_conversion

    ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
    roi = ((total_revenue - total_cost) / total_cost * 100) if total_cost > 0 else 0
    cpc = total_cost / total_clicks if total_clicks > 0 else 0
    cpa = total_cost / total_conversions if total_conversions > 0 else 0
    roas = total_revenue / total_cost if total_cost > 0 else 0

    # Best performing posts
    best_posts = sorted(posts, key=lambda p: p.get('likes', 0) + p.get('retweets', 0), reverse=True)[:5]

    # Time-based performance
    hourly = {}
    for post in posts:
        date_str = str(post.get('posted_at', ''))
        if len(date_str) >= 13:
            try:
                hour = int(date_str[11:13])
                eng = post.get('likes', 0) + post.get('retweets', 0)
                hourly[hour] = hourly.get(hour, 0) + eng
            except (ValueError, IndexError):
                pass

    best_hour = max(hourly, key=hourly.get) if hourly else 12
    worst_hour = min(hourly, key=hourly.get) if hourly else 3

    # Budget recommendations
    avg_engagement = total_clicks / len(posts) if posts else 0
    budget_recommendation = 'Increase budget' if roi > 100 else 'Optimize targeting' if roi > 0 else 'Review strategy'

    return {
        'metrics': {
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'total_conversions': total_conversions,
            'total_cost': round(total_cost, 2),
            'total_revenue': round(total_revenue, 2),
            'ctr': round(ctr, 3),
            'conversion_rate': round(conversion_rate, 2),
            'roi': round(roi, 2),
            'cpc': round(cpc, 4),
            'cpa': round(cpa, 2),
            'roas': round(roas, 2),
        },
        'performance_grade': 'A' if roi > 200 else 'B' if roi > 100 else 'C' if roi > 0 else 'D',
        'best_performing_posts': [
            {
                'text': p['text'][:100],
                'author': p.get('author', ''),
                'engagement': p.get('likes', 0) + p.get('retweets', 0),
                'estimated_ctr': round((p.get('likes', 0) / max(p.get('author_followers', 1), 1)) * 100, 3)
            }
            for p in best_posts
        ],
        'timing_insights': {
            'best_hour': f'{best_hour:02d}:00',
            'worst_hour': f'{worst_hour:02d}:00',
            'hourly_engagement': [{'hour': f'{h:02d}:00', 'engagement': hourly.get(h, 0)} for h in range(24)],
        },
        'recommendations': [
            f'Best posting time: {best_hour:02d}:00',
            f'Current ROI: {roi:.1f}% — {budget_recommendation}',
            f'Average engagement per post: {avg_engagement:.0f} interactions',
            'Focus on authors with >10K followers for higher reach',
            'Use 3-5 relevant hashtags per post for best discovery',
        ],
        'budget_recommendation': budget_recommendation,
    }

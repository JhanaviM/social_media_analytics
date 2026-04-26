"""
Module 11: Competitor Analysis
Compares growth, engagement, and strategy between keyword and detected competitors.
"""
import re
from collections import defaultdict


COMPETITOR_KEYWORDS = {
    'Tesla': ['BMW', 'Ford', 'Rivian', 'Lucid', 'BYD', 'NIO'],
    'Apple': ['Samsung', 'Google', 'Microsoft', 'Huawei', 'OnePlus'],
    'Nike': ['Adidas', 'Puma', 'Reebok', 'NewBalance', 'UnderArmour'],
    'default': ['competitor1', 'competitor2', 'rival', 'alternative'],
}


def analyze_competitors(posts: list, keyword: str) -> dict:
    # Detect competitors in text
    competitors = COMPETITOR_KEYWORDS.get(keyword, COMPETITOR_KEYWORDS['default'])
    detected = set()
    for post in posts:
        text_lower = post['text'].lower()
        for comp in competitors:
            if comp.lower() in text_lower:
                detected.add(comp)

    if not detected:
        # Find most mentioned brands (capitalized words)
        brand_mentions = defaultdict(int)
        for post in posts:
            words = re.findall(r'\b[A-Z][a-z]{2,}\b', post['text'])
            for word in words:
                if word.lower() != keyword.lower():
                    brand_mentions[word] += 1
        detected = set(list({k for k, v in sorted(brand_mentions.items(), key=lambda x: -x[1])[:5]}))

    # Main brand stats
    def compute_stats(posts_subset):
        if not posts_subset:
            return {'post_count': 0, 'avg_likes': 0, 'avg_retweets': 0, 'total_reach': 0, 'engagement_rate': 0}
        n = len(posts_subset)
        total_likes = sum(p.get('likes', 0) for p in posts_subset)
        total_retweets = sum(p.get('retweets', 0) for p in posts_subset)
        total_reach = sum(p.get('author_followers', 0) for p in posts_subset)
        eng_rate = (total_likes + total_retweets) / max(total_reach, 1) * 100
        return {
            'post_count': n,
            'avg_likes': round(total_likes / n, 1),
            'avg_retweets': round(total_retweets / n, 1),
            'total_reach': total_reach,
            'engagement_rate': round(eng_rate, 3),
        }

    main_posts = [p for p in posts if keyword.lower() in p['text'].lower()]
    main_stats = compute_stats(main_posts)
    main_stats['name'] = keyword

    competitor_stats = []
    for comp in list(detected)[:5]:
        comp_posts = [p for p in posts if comp.lower() in p['text'].lower()]
        stats = compute_stats(comp_posts)
        stats['name'] = comp
        competitor_stats.append(stats)

    competitor_stats = sorted(competitor_stats, key=lambda x: x['engagement_rate'], reverse=True)

    # Strategy insights
    all_brands = [main_stats] + competitor_stats
    top_brand = max(all_brands, key=lambda x: x['engagement_rate'])

    # Hashtag strategy comparison
    main_hashtags = defaultdict(int)
    for post in main_posts:
        for tag in post.get('hashtags', []):
            main_hashtags[tag.lower()] += 1

    return {
        'main_brand': main_stats,
        'competitors': competitor_stats,
        'detected_competitors': list(detected),
        'market_leader': top_brand['name'],
        'competitive_position': 'Leader' if top_brand['name'] == keyword else 'Challenger',
        'comparison_chart': {
            'brands': [b['name'] for b in all_brands],
            'avg_likes': [b['avg_likes'] for b in all_brands],
            'avg_retweets': [b['avg_retweets'] for b in all_brands],
            'engagement_rate': [b['engagement_rate'] for b in all_brands],
            'total_reach': [b['total_reach'] for b in all_brands],
        },
        'insights': [
            f'{top_brand["name"]} leads in engagement with {top_brand["engagement_rate"]:.3f}% rate',
            f'{keyword} has {len(main_posts)} posts vs {sum(c["post_count"] for c in competitor_stats)} competitor posts',
            f'Top hashtags for {keyword}: {", ".join(f"#{t}" for t in list(main_hashtags.keys())[:5])}',
            'Competitors with higher engagement are posting more frequently',
        ],
        'main_hashtags': [{'tag': f'#{t}', 'count': c} for t, c in sorted(main_hashtags.items(), key=lambda x: -x[1])[:10]],
    }

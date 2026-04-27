"""Module 6: User Segmentation — KMeans, no pandas."""
from collections import defaultdict

SEGMENT_LABELS = {
    0: {'name': 'Power Users',      'color': '#6C63FF', 'description': 'High followers, high engagement'},
    1: {'name': 'Casual Engagers',  'color': '#48CAE4', 'description': 'Moderate activity, low followers'},
    2: {'name': 'Lurkers',          'color': '#90BE6D', 'description': 'Low engagement, rarely post'},
    3: {'name': 'Micro-Influencers','color': '#F9C74F', 'description': 'Small but highly engaged audience'},
    4: {'name': 'Brand Advocates',  'color': '#F3722C', 'description': 'Frequent posters, positive sentiment'},
}


def segment_users(posts: list) -> dict:
    try:
        import numpy as np
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler

        author_data = defaultdict(lambda: {'posts': 0, 'likes': 0, 'retweets': 0, 'replies': 0, 'followers': 0, 'hashtags': 0})
        for post in posts:
            a = post.get('author', 'unknown')
            author_data[a]['posts']     += 1
            author_data[a]['likes']     += post.get('likes', 0)
            author_data[a]['retweets']  += post.get('retweets', 0)
            author_data[a]['replies']   += post.get('replies', 0)
            author_data[a]['followers']  = max(author_data[a]['followers'], post.get('author_followers', 0))
            author_data[a]['hashtags']  += len(post.get('hashtags', []))

        if len(author_data) < 3:
            return {'error': 'Not enough unique authors', 'segments': []}

        authors = list(author_data.keys())
        features = []
        for a in authors:
            d = author_data[a]
            p = max(d['posts'], 1)
            features.append([d['followers'], d['likes']/p, d['retweets']/p, d['posts'], d['hashtags']/p])

        X = np.array(features, dtype=float)
        X_s = StandardScaler().fit_transform(X)
        n_clusters = min(5, len(authors))
        labels = KMeans(n_clusters=n_clusters, random_state=42, n_init=10).fit_predict(X_s)

        segments_map = defaultdict(list)
        user_results = []
        for i, author in enumerate(authors):
            seg_id  = int(labels[i])
            seg_inf = SEGMENT_LABELS.get(seg_id, {'name': f'Segment {seg_id}', 'color': '#ccc', 'description': ''})
            d = author_data[author]
            info = {
                'author': author, 'segment_id': seg_id,
                'segment_name': seg_inf['name'], 'segment_color': seg_inf['color'],
                'followers': d['followers'], 'total_likes': d['likes'],
                'total_retweets': d['retweets'], 'post_count': d['posts'],
                'avg_likes': round(d['likes'] / max(d['posts'], 1), 1),
            }
            segments_map[seg_inf['name']].append(info)
            user_results.append(info)

        segment_summary = []
        for seg_name, users in segments_map.items():
            seg_id  = users[0]['segment_id']
            seg_inf = SEGMENT_LABELS.get(seg_id, {'color': '#ccc', 'description': ''})
            segment_summary.append({
                'name': seg_name, 'count': len(users),
                'color': seg_inf['color'], 'description': seg_inf['description'],
                'avg_followers': round(sum(u['followers'] for u in users) / len(users)),
                'avg_likes':     round(sum(u['avg_likes'] for u in users) / len(users), 1),
                'sample_users':  [u['author'] for u in users[:3]],
            })

        return {
            'total_users': len(authors), 'n_clusters': n_clusters,
            'segments': sorted(segment_summary, key=lambda x: x['count'], reverse=True),
            'user_details': sorted(user_results, key=lambda x: x['followers'], reverse=True)[:30],
            'scatter_data': [
                {'x': features[i][0], 'y': features[i][1],
                 'label': SEGMENT_LABELS.get(int(labels[i]), {}).get('name', f'Seg {labels[i]}'),
                 'author': authors[i]}
                for i in range(len(authors))
            ]
        }
    except Exception as e:
        return {'error': str(e), 'segments': []}

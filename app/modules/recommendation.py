"""
Module 4: Recommendation System
Content-based + collaborative filtering for post/content recommendations.
"""
import re
import math
from collections import defaultdict


def get_recommendations(posts: list, keyword: str) -> dict:
    try:
        if len(posts) < 2:
            return {'error': 'Not enough posts for recommendations', 'recommendations': []}

        # ── Content-Based Filtering ───────────────────────────────────────────
        # TF-IDF style scoring without sklearn dependency issues
        def tokenize(text):
            text = re.sub(r'http\S+|@\w+|#', '', text.lower())
            return re.findall(r'\b[a-zA-Z]{3,}\b', text)

        docs = [tokenize(p['text']) for p in posts]

        # Term frequency per doc
        tf = []
        for doc in docs:
            counts = defaultdict(int)
            for word in doc:
                counts[word] += 1
            total = len(doc) or 1
            tf.append({w: c / total for w, c in counts.items()})

        # Document frequency
        df = defaultdict(int)
        for doc in docs:
            for word in set(doc):
                df[word] += 1

        N = len(docs)

        # TF-IDF vectors
        tfidf = []
        for tf_doc in tf:
            vec = {}
            for word, freq in tf_doc.items():
                idf = math.log((N + 1) / (df[word] + 1)) + 1
                vec[word] = freq * idf
            tfidf.append(vec)

        # Cosine similarity
        def cosine_sim(v1, v2):
            common = set(v1) & set(v2)
            if not common:
                return 0.0
            dot = sum(v1[w] * v2[w] for w in common)
            mag1 = math.sqrt(sum(x ** 2 for x in v1.values()))
            mag2 = math.sqrt(sum(x ** 2 for x in v2.values()))
            return dot / (mag1 * mag2) if mag1 * mag2 > 0 else 0.0

        # Recommend based on top-engagement post
        anchor_idx = max(range(len(posts)), key=lambda i: posts[i].get('likes', 0))
        anchor_vec = tfidf[anchor_idx]

        content_recs = []
        for i, post in enumerate(posts):
            if i == anchor_idx:
                continue
            sim = cosine_sim(anchor_vec, tfidf[i])
            content_recs.append({
                'text': post['text'][:100],
                'author': post.get('author', ''),
                'similarity': round(sim, 3),
                'likes': post.get('likes', 0),
            })

        content_recs = sorted(content_recs, key=lambda x: x['similarity'], reverse=True)[:10]

        # ── Collaborative Filtering (engagement-based) ────────────────────────
        author_engagement = defaultdict(lambda: {'likes': 0, 'retweets': 0, 'posts': 0})
        for post in posts:
            a = post.get('author', 'unknown')
            author_engagement[a]['likes'] += post.get('likes', 0)
            author_engagement[a]['retweets'] += post.get('retweets', 0)
            author_engagement[a]['posts'] += 1

        collab_recs = []
        for author, stats in author_engagement.items():
            score = (stats['likes'] * 1.0 + stats['retweets'] * 1.5) / max(stats['posts'], 1)
            collab_recs.append({
                'author': author,
                'avg_engagement_score': round(score, 2),
                'total_likes': stats['likes'],
                'total_retweets': stats['retweets'],
                'post_count': stats['posts'],
            })

        collab_recs = sorted(collab_recs, key=lambda x: x['avg_engagement_score'], reverse=True)[:10]

        # ── Keyword-based content suggestions ────────────────────────────────
        kw_lower = keyword.lower()
        keyword_matches = [
            {'text': p['text'][:100], 'author': p.get('author', ''), 'relevance': 'high'}
            for p in posts if kw_lower in p['text'].lower()
        ][:10]

        return {
            'anchor_post': posts[anchor_idx]['text'][:120],
            'content_based': content_recs,
            'collaborative': collab_recs,
            'keyword_matches': keyword_matches,
            'summary': {
                'total_analyzed': len(posts),
                'top_recommended_author': collab_recs[0]['author'] if collab_recs else '',
                'keyword': keyword,
            }
        }
    except Exception as e:
        return {'error': str(e), 'recommendations': []}

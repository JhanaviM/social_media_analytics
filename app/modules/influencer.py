"""
Module 9: Influencer Detection
Uses Eigenvector Centrality + engagement metrics to rank influencers.
"""
import re
from collections import defaultdict


def detect_influencers(posts: list) -> dict:
    try:
        import networkx as nx

        G = nx.DiGraph()
        author_stats = defaultdict(lambda: {
            'posts': 0, 'likes': 0, 'retweets': 0,
            'replies': 0, 'followers': 0, 'mentions_received': 0
        })

        for post in posts:
            author = post.get('author', 'unknown')
            author_stats[author]['posts'] += 1
            author_stats[author]['likes'] += post.get('likes', 0)
            author_stats[author]['retweets'] += post.get('retweets', 0)
            author_stats[author]['replies'] += post.get('replies', 0)
            author_stats[author]['followers'] = max(
                author_stats[author]['followers'],
                post.get('author_followers', 0)
            )
            G.add_node(author)
            mentions = re.findall(r'@(\w+)', post['text'])
            for m in mentions:
                G.add_edge(author, m.lower())
                author_stats[m.lower()]['mentions_received'] += 1

        if G.number_of_nodes() < 2:
            # Fallback: rank by engagement only
            ranked = []
            for author, stats in author_stats.items():
                eng_score = stats['likes'] * 1 + stats['retweets'] * 1.5 + stats['replies'] * 0.5
                ranked.append({'author': author, 'engagement_score': round(eng_score, 2), **stats})
            ranked = sorted(ranked, key=lambda x: x['engagement_score'], reverse=True)[:10]
            return {'influencers': ranked, 'method': 'engagement_only', 'total_analyzed': len(author_stats)}

        # Eigenvector centrality
        try:
            eigen = nx.eigenvector_centrality(G, max_iter=200, tol=1e-4)
        except Exception:
            eigen = {n: 0.0 for n in G.nodes()}

        try:
            pagerank = nx.pagerank(G, max_iter=100)
        except Exception:
            pagerank = {n: 0.0 for n in G.nodes()}

        influencer_list = []
        for author in author_stats:
            stats = author_stats[author]
            eng_per_post = (stats['likes'] + stats['retweets'] * 1.5) / max(stats['posts'], 1)
            eig_score = eigen.get(author, 0)
            pr_score = pagerank.get(author, 0)
            followers = stats['followers']

            # Composite influencer score
            influence_score = (
                eig_score * 40 +
                pr_score * 30 +
                (min(eng_per_post, 1000) / 1000) * 20 +
                (min(followers, 1_000_000) / 1_000_000) * 10
            )

            influencer_list.append({
                'author': author,
                'influence_score': round(influence_score * 100, 2),
                'eigenvector_centrality': round(eig_score, 6),
                'pagerank': round(pr_score, 6),
                'followers': followers,
                'total_likes': stats['likes'],
                'total_retweets': stats['retweets'],
                'post_count': stats['posts'],
                'mentions_received': stats['mentions_received'],
                'avg_engagement': round(eng_per_post, 1),
                'tier': (
                    'Mega (1M+)' if followers >= 1_000_000 else
                    'Macro (100K-1M)' if followers >= 100_000 else
                    'Mid (10K-100K)' if followers >= 10_000 else
                    'Micro (1K-10K)' if followers >= 1_000 else
                    'Nano (<1K)'
                )
            })

        influencer_list = sorted(influencer_list, key=lambda x: x['influence_score'], reverse=True)

        tier_counts = defaultdict(int)
        for inf in influencer_list:
            tier_counts[inf['tier']] += 1

        return {
            'total_analyzed': len(influencer_list),
            'top_influencers': influencer_list[:15],
            'tier_distribution': dict(tier_counts),
            'top_by_reach': sorted(influencer_list, key=lambda x: x['followers'], reverse=True)[:5],
            'top_by_engagement': sorted(influencer_list, key=lambda x: x['avg_engagement'], reverse=True)[:5],
            'network_stats': {
                'nodes': G.number_of_nodes(),
                'edges': G.number_of_edges(),
            }
        }
    except Exception as e:
        return {'error': str(e), 'influencers': []}

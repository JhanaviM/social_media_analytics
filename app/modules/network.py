"""
Module 3: Network Analysis
Builds author interaction graphs, detects communities and influencers using NetworkX.
"""
import re


def analyze_network(posts: list) -> dict:
    try:
        import networkx as nx
        from collections import defaultdict

        G = nx.DiGraph()
        author_stats = defaultdict(lambda: {'posts': 0, 'likes': 0, 'retweets': 0, 'followers': 0})
        mention_edges = []

        for post in posts:
            author = post.get('author', 'unknown')
            if not author:
                continue

            author_stats[author]['posts'] += 1
            author_stats[author]['likes'] += post.get('likes', 0)
            author_stats[author]['retweets'] += post.get('retweets', 0)
            author_stats[author]['followers'] = max(
                author_stats[author]['followers'],
                post.get('author_followers', 0)
            )

            G.add_node(author,
                       followers=post.get('author_followers', 0),
                       posts=author_stats[author]['posts'])

            mentions = re.findall(r'@(\w+)', post['text'])
            for mentioned in mentions:
                mentioned = mentioned.lower()
                G.add_edge(author, mentioned, weight=1)
                mention_edges.append({'from': author, 'to': mentioned})

        # Centrality scores
        if G.number_of_nodes() > 0:
            try:
                degree_centrality = nx.degree_centrality(G)
                betweenness = nx.betweenness_centrality(G, k=min(50, G.number_of_nodes()))
                if G.number_of_nodes() > 1:
                    eigenvector = nx.eigenvector_centrality(G, max_iter=100, tol=1e-3)
                else:
                    eigenvector = {n: 0 for n in G.nodes()}
            except Exception:
                degree_centrality = {n: 0 for n in G.nodes()}
                betweenness = {n: 0 for n in G.nodes()}
                eigenvector = {n: 0 for n in G.nodes()}

            # Community detection (simple: group by degree)
            nodes_data = []
            for node in list(G.nodes())[:50]:
                nodes_data.append({
                    'id': node,
                    'degree': G.degree(node),
                    'degree_centrality': round(degree_centrality.get(node, 0), 4),
                    'betweenness': round(betweenness.get(node, 0), 4),
                    'eigenvector': round(eigenvector.get(node, 0), 4),
                    'followers': author_stats[node]['followers'],
                    'posts': author_stats[node]['posts'],
                })

            # Top influencers by eigenvector centrality
            influencers = sorted(nodes_data, key=lambda x: x['eigenvector'], reverse=True)[:10]

            # Connectors by betweenness
            connectors = sorted(nodes_data, key=lambda x: x['betweenness'], reverse=True)[:5]

            # Communities (simple partitioning by degree quartiles)
            degrees = sorted([n['degree'] for n in nodes_data])
            if degrees:
                q1 = degrees[len(degrees) // 4]
                q3 = degrees[3 * len(degrees) // 4]
                communities = {
                    'high_influence': [n['id'] for n in nodes_data if n['degree'] >= q3],
                    'medium_influence': [n['id'] for n in nodes_data if q1 <= n['degree'] < q3],
                    'low_influence': [n['id'] for n in nodes_data if n['degree'] < q1],
                }
            else:
                communities = {'high_influence': [], 'medium_influence': [], 'low_influence': []}

            # Graph edges for visualization
            edges_data = [{'from': u, 'to': v} for u, v in list(G.edges())[:100]]

        else:
            nodes_data = []
            influencers = []
            connectors = []
            communities = {}
            edges_data = []

        return {
            'total_nodes': G.number_of_nodes(),
            'total_edges': G.number_of_edges(),
            'density': round(nx.density(G), 4) if G.number_of_nodes() > 1 else 0,
            'top_influencers': influencers,
            'top_connectors': connectors,
            'communities': communities,
            'nodes': nodes_data[:50],
            'edges': edges_data[:100],
            'graph_stats': {
                'avg_degree': round(sum(dict(G.degree()).values()) / max(G.number_of_nodes(), 1), 2),
                'max_degree': max(dict(G.degree()).values()) if G.number_of_nodes() > 0 else 0,
            }
        }
    except Exception as e:
        return {'error': str(e), 'total_nodes': 0, 'total_edges': 0}

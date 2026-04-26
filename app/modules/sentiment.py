"""
Module 1: Sentiment Analysis
Uses NLTK VADER for fast rule-based sentiment + optional HuggingFace for deep analysis.
"""
import re
from collections import Counter


def clean_text(text: str) -> str:
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = re.sub(r'#', '', text)
    return text.strip()


def analyze_sentiment(posts: list) -> dict:
    try:
        import nltk
        try:
            from nltk.sentiment.vader import SentimentIntensityAnalyzer
        except LookupError:
            nltk.download('vader_lexicon', quiet=True)
            from nltk.sentiment.vader import SentimentIntensityAnalyzer

        sia = SentimentIntensityAnalyzer()
        results = []
        label_counts = Counter()
        scores_over_time = []

        for post in posts:
            text = clean_text(post['text'])
            scores = sia.polarity_scores(text)
            compound = scores['compound']

            if compound >= 0.05:
                label = 'Positive'
            elif compound <= -0.05:
                label = 'Negative'
            else:
                label = 'Neutral'

            label_counts[label] += 1
            results.append({
                'text': post['text'][:120],
                'author': post.get('author', ''),
                'label': label,
                'score': round(compound, 3),
                'pos': round(scores['pos'], 3),
                'neg': round(scores['neg'], 3),
                'neu': round(scores['neu'], 3),
            })

            scores_over_time.append({
                'date': post.get('posted_at', ''),
                'score': round(compound, 3),
                'label': label
            })

        total = len(results)
        return {
            'total_posts': total,
            'distribution': {
                'Positive': label_counts['Positive'],
                'Negative': label_counts['Negative'],
                'Neutral': label_counts['Neutral'],
            },
            'percentages': {
                'Positive': round(label_counts['Positive'] / total * 100, 1) if total else 0,
                'Negative': round(label_counts['Negative'] / total * 100, 1) if total else 0,
                'Neutral': round(label_counts['Neutral'] / total * 100, 1) if total else 0,
            },
            'average_score': round(sum(r['score'] for r in results) / total, 3) if total else 0,
            'top_positive': sorted([r for r in results if r['label'] == 'Positive'], key=lambda x: x['score'], reverse=True)[:5],
            'top_negative': sorted([r for r in results if r['label'] == 'Negative'], key=lambda x: x['score'])[:5],
            'timeline': scores_over_time[:50],
            'all_results': results[:100],
        }
    except Exception as e:
        return {'error': str(e), 'total_posts': len(posts)}

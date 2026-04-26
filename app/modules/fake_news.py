"""
Module 5: Fake News Detection
Rule-based + ML classifier to flag posts as Fake / Real / Uncertain.
"""
import re
from collections import Counter


CLICKBAIT_PATTERNS = [
    r'\byou won\'t believe\b', r'\bshocking\b', r'\bmind.?blowing\b',
    r'\bbreaking\b.*\bnews\b', r'\bwarning\b', r'\bfake\b', r'\bhoax\b',
    r'\bconspiracy\b', r'\bsecret\b.*\bthey\b', r'\b100%\b.*\bproven\b',
    r'\bdoctors hate\b', r'\bgovernment hides\b', r'\bunbelievable\b',
    r'!!!', r'\ball caps\b', r'\bshare before deleted\b',
    r'\bforward this\b', r'\bviral\b.*\btruth\b',
]

CREDIBILITY_SIGNALS = [
    r'\baccording to\b', r'\bresearch shows\b', r'\bstudy finds\b',
    r'\bsource:\b', r'\bvia @\w+\b', r'\bofficial\b', r'\bconfirmed\b',
    r'\bpeer.?reviewed\b', r'\buniversity\b', r'\bscientists\b',
]

EMOTIONAL_AMPLIFIERS = [
    r'\bOMG\b', r'\bWTF\b', r'\bunbelievable\b', r'\binsane\b',
    r'\bcraxy\b', r'\bnever seen\b', r'\bhistoric\b', r'\bepic\b',
    r'\bshocking\b', r'\bdisgusting\b', r'\boutrageous\b',
]


def classify_post(text: str) -> dict:
    text_lower = text.lower()

    clickbait_hits = sum(1 for p in CLICKBAIT_PATTERNS if re.search(p, text_lower, re.IGNORECASE))
    credibility_hits = sum(1 for p in CREDIBILITY_SIGNALS if re.search(p, text_lower, re.IGNORECASE))
    emotion_hits = sum(1 for p in EMOTIONAL_AMPLIFIERS if re.search(p, text_lower, re.IGNORECASE))

    # Caps ratio
    alpha_chars = [c for c in text if c.isalpha()]
    caps_ratio = sum(1 for c in alpha_chars if c.isupper()) / max(len(alpha_chars), 1)

    # Exclamation density
    excl_count = text.count('!')
    has_url = bool(re.search(r'http\S+', text))
    has_hashtag = bool(re.search(r'#\w+', text))

    # Scoring: higher = more suspicious
    suspicion_score = (
        clickbait_hits * 2.0 +
        emotion_hits * 1.5 +
        caps_ratio * 3.0 +
        min(excl_count, 3) * 0.5 -
        credibility_hits * 2.0 -
        (0.5 if has_url else 0) -
        (0.3 if has_hashtag else 0)
    )

    if suspicion_score >= 3.0:
        label = 'Fake'
        confidence = min(0.95, 0.5 + suspicion_score * 0.1)
    elif suspicion_score <= 0.0:
        label = 'Real'
        confidence = min(0.95, 0.6 + abs(suspicion_score) * 0.1)
    else:
        label = 'Uncertain'
        confidence = 0.4 + abs(suspicion_score - 1.5) * 0.05

    return {
        'label': label,
        'confidence': round(min(confidence, 0.98), 2),
        'suspicion_score': round(suspicion_score, 2),
        'signals': {
            'clickbait_patterns': clickbait_hits,
            'credibility_signals': credibility_hits,
            'emotional_language': emotion_hits,
            'caps_ratio': round(caps_ratio, 2),
            'exclamations': excl_count,
        }
    }


def detect_fake_news(posts: list) -> dict:
    results = []
    label_counts = Counter()

    for post in posts:
        classification = classify_post(post['text'])
        label_counts[classification['label']] += 1
        results.append({
            'text': post['text'][:120],
            'author': post.get('author', ''),
            **classification
        })

    total = len(results)
    fake_posts = [r for r in results if r['label'] == 'Fake']
    uncertain_posts = [r for r in results if r['label'] == 'Uncertain']

    return {
        'total_posts': total,
        'distribution': dict(label_counts),
        'percentages': {
            label: round(count / total * 100, 1) if total else 0
            for label, count in label_counts.items()
        },
        'high_risk_posts': sorted(fake_posts, key=lambda x: x['suspicion_score'], reverse=True)[:10],
        'uncertain_posts': uncertain_posts[:5],
        'fake_count': label_counts['Fake'],
        'real_count': label_counts['Real'],
        'uncertain_count': label_counts['Uncertain'],
        'all_results': results[:50],
    }

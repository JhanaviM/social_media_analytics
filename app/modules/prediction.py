"""Module 12: Popularity Prediction — Random Forest, no pandas."""
import re

FEATURE_NAMES = ['text_length','exclamations','questions','hashtag_count',
                 'mention_count','has_url','author_followers','word_count','caps_ratio']

def extract_features(post):
    text = post.get('text', '')
    alpha = [c for c in text if c.isalpha()]
    return [
        len(text),
        text.count('!'),
        text.count('?'),
        len(re.findall(r'#\w+', text)),
        len(re.findall(r'@\w+', text)),
        1 if re.search(r'http\S+', text) else 0,
        post.get('author_followers', 0),
        len(text.split()),
        sum(1 for c in alpha if c.isupper()) / max(len(alpha), 1),
    ]

def predict_popularity(posts):
    try:
        import numpy as np
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.metrics import mean_squared_error, r2_score

        if len(posts) < 10:
            return {'error': 'Need at least 10 posts', 'predictions': []}

        X = np.array([extract_features(p) for p in posts], dtype=float)
        y = np.array([p.get('likes',0)*1.0 + p.get('retweets',0)*1.5 + p.get('replies',0)*0.5 for p in posts])

        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_tr_s = scaler.fit_transform(X_tr)
        X_te_s = scaler.transform(X_te)

        rf = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=6)
        rf.fit(X_tr_s, y_tr)
        rf_pred = rf.predict(X_te_s)
        rf_r2   = r2_score(y_te, rf_pred)
        rf_rmse = float(mean_squared_error(y_te, rf_pred)**0.5)

        gb = GradientBoostingRegressor(n_estimators=100, random_state=42, max_depth=4)
        gb.fit(X_tr_s, y_tr)
        gb_r2 = r2_score(y_te, gb.predict(X_te_s))

        all_pred = rf.predict(scaler.transform(X))
        importance = sorted(
            [{'feature': FEATURE_NAMES[i], 'importance': round(float(rf.feature_importances_[i]), 4)}
             for i in range(len(FEATURE_NAMES))],
            key=lambda x: x['importance'], reverse=True
        )

        predictions = [
            {'text': posts[i]['text'][:100], 'author': posts[i].get('author',''),
             'actual_engagement': round(float(y[i]),1), 'predicted_engagement': round(float(all_pred[i]),1),
             'error': round(abs(float(y[i])-float(all_pred[i])),1)}
            for i in range(min(30, len(posts)))
        ]

        future_scenarios = [
            {'scenario': 'Short post with 3 hashtags',        'features': [80,1,0,3,1,0,5000,12,0.05],    'predicted': 0},
            {'scenario': 'Long post with URL and mentions',   'features': [280,0,1,5,3,1,50000,45,0.02],  'predicted': 0},
            {'scenario': 'Viral-style exclamation post',      'features': [150,3,0,6,2,0,100000,25,0.15], 'predicted': 0},
        ]
        for sc in future_scenarios:
            sc['predicted'] = round(float(rf.predict(scaler.transform([sc['features']]))[0]), 1)

        return {
            'model_performance': {
                'random_forest_r2': round(rf_r2, 3), 'random_forest_rmse': round(rf_rmse, 2),
                'gradient_boosting_r2': round(gb_r2, 3),
                'best_model': 'Random Forest' if rf_r2 >= gb_r2 else 'Gradient Boosting',
            },
            'feature_importance': importance,
            'predictions': sorted(predictions, key=lambda x: x['predicted_engagement'], reverse=True),
            'future_scenarios': future_scenarios,
            'top_predicted_posts': sorted(predictions, key=lambda x: x['predicted_engagement'], reverse=True)[:5],
            'actual_vs_predicted': [
                {'actual': round(float(y_te[i]),1), 'predicted': round(float(rf_pred[i]),1)}
                for i in range(len(y_te))
            ],
        }
    except Exception as e:
        return {'error': str(e), 'predictions': []}

"""
Module 12: Popularity Prediction
Uses Random Forest to predict engagement score based on post features.
"""
import re


def extract_features(post: dict) -> list:
    text = post.get('text', '')
    return [
        len(text),
        text.count('!'),
        text.count('?'),
        len(re.findall(r'#\w+', text)),
        len(re.findall(r'@\w+', text)),
        1 if re.search(r'http\S+', text) else 0,
        post.get('author_followers', 0),
        len(text.split()),
        sum(1 for c in text if c.isupper()) / max(len(text), 1),
    ]


FEATURE_NAMES = [
    'text_length', 'exclamations', 'questions', 'hashtag_count',
    'mention_count', 'has_url', 'author_followers', 'word_count', 'caps_ratio'
]


def predict_popularity(posts: list) -> dict:
    try:
        import numpy as np
        from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        from sklearn.metrics import mean_squared_error, r2_score

        if len(posts) < 10:
            return {'error': 'Need at least 10 posts for prediction', 'predictions': []}

        X = np.array([extract_features(p) for p in posts])
        y = np.array([
            p.get('likes', 0) * 1.0 + p.get('retweets', 0) * 1.5 + p.get('replies', 0) * 0.5
            for p in posts
        ])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train_s = scaler.fit_transform(X_train)
        X_test_s = scaler.transform(X_test)

        # Random Forest
        rf = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=6)
        rf.fit(X_train_s, y_train)
        rf_preds = rf.predict(X_test_s)
        rf_r2 = r2_score(y_test, rf_preds)
        rf_rmse = mean_squared_error(y_test, rf_preds) ** 0.5

        # Gradient Boosting
        gb = GradientBoostingRegressor(n_estimators=100, random_state=42, max_depth=4)
        gb.fit(X_train_s, y_train)
        gb_preds = gb.predict(X_test_s)
        gb_r2 = r2_score(y_test, gb_preds)

        # Best model predictions on ALL posts
        X_all_s = scaler.transform(X)
        all_preds = rf.predict(X_all_s)

        # Feature importance
        importance = rf.feature_importances_
        feature_importance = sorted(
            [{'feature': FEATURE_NAMES[i], 'importance': round(float(importance[i]), 4)}
             for i in range(len(FEATURE_NAMES))],
            key=lambda x: x['importance'], reverse=True
        )

        predictions = []
        for i, post in enumerate(posts[:30]):
            predictions.append({
                'text': post['text'][:100],
                'author': post.get('author', ''),
                'actual_engagement': round(float(y[i]), 1),
                'predicted_engagement': round(float(all_preds[i]), 1),
                'error': round(abs(float(y[i]) - float(all_preds[i])), 1),
            })

        # Future predictions (hypothetical posts)
        future_scenarios = [
            {
                'scenario': 'Short post with 3 hashtags',
                'features': [80, 1, 0, 3, 1, 0, 5000, 12, 0.05],
                'predicted': 0,
            },
            {
                'scenario': 'Long post with URL and mentions',
                'features': [280, 0, 1, 5, 3, 1, 50000, 45, 0.02],
                'predicted': 0,
            },
            {
                'scenario': 'Viral-style exclamation post',
                'features': [150, 3, 0, 6, 2, 0, 100000, 25, 0.15],
                'predicted': 0,
            },
        ]

        for scenario in future_scenarios:
            feat_arr = scaler.transform([scenario['features']])
            scenario['predicted'] = round(float(rf.predict(feat_arr)[0]), 1)

        return {
            'model_performance': {
                'random_forest_r2': round(rf_r2, 3),
                'random_forest_rmse': round(rf_rmse, 2),
                'gradient_boosting_r2': round(gb_r2, 3),
                'best_model': 'Random Forest' if rf_r2 >= gb_r2 else 'Gradient Boosting',
            },
            'feature_importance': feature_importance,
            'predictions': sorted(predictions, key=lambda x: x['predicted_engagement'], reverse=True),
            'future_scenarios': future_scenarios,
            'top_predicted_posts': sorted(predictions, key=lambda x: x['predicted_engagement'], reverse=True)[:5],
            'actual_vs_predicted': [
                {'actual': round(float(y_test[i]), 1), 'predicted': round(float(rf_preds[i]), 1)}
                for i in range(len(y_test))
            ],
        }
    except Exception as e:
        return {'error': str(e), 'predictions': []}

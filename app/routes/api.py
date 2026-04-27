@api.route('/run-all/<int:case_id>', methods=['POST'])
@login_required
def run_all(case_id):
    """Run all modules one by one with error isolation."""
    case, posts = get_case_posts(case_id)
    if not posts:
        return jsonify({'error': 'No posts found. Load data first.'}), 400

    results = {}

    # Run each module individually so one failure doesn't kill the rest
    try:
        from app.modules.sentiment import analyze_sentiment
        r = analyze_sentiment(posts)
        save_result(case_id, 'sentiment', r)
        results['sentiment'] = 'ok'
    except Exception as e:
        results['sentiment'] = str(e)

    try:
        from app.modules.trending import detect_trends
        r = detect_trends(posts)
        save_result(case_id, 'trending', r)
        results['trending'] = 'ok'
    except Exception as e:
        results['trending'] = str(e)

    try:
        from app.modules.network import analyze_network
        r = analyze_network(posts)
        save_result(case_id, 'network', r)
        results['network'] = 'ok'
    except Exception as e:
        results['network'] = str(e)

    try:
        from app.modules.recommendation import get_recommendations
        r = get_recommendations(posts, case.keyword)
        save_result(case_id, 'recommendation', r)
        results['recommendation'] = 'ok'
    except Exception as e:
        results['recommendation'] = str(e)

    try:
        from app.modules.fake_news import detect_fake_news
        r = detect_fake_news(posts)
        save_result(case_id, 'fakenews', r)
        results['fakenews'] = 'ok'
    except Exception as e:
        results['fakenews'] = str(e)

    try:
        from app.modules.segmentation import segment_users
        r = segment_users(posts)
        save_result(case_id, 'segmentation', r)
        results['segmentation'] = 'ok'
    except Exception as e:
        results['segmentation'] = str(e)

    try:
        from app.modules.visualization import build_charts
        r = build_charts(posts)
        save_result(case_id, 'visualization', r)
        results['visualization'] = 'ok'
    except Exception as e:
        results['visualization'] = str(e)

    try:
        from app.modules.ads import optimize_ads
        r = optimize_ads(posts)
        save_result(case_id, 'ads', r)
        results['ads'] = 'ok'
    except Exception as e:
        results['ads'] = str(e)

    try:
        from app.modules.influencer import detect_influencers
        r = detect_influencers(posts)
        save_result(case_id, 'influencer', r)
        results['influencer'] = 'ok'
    except Exception as e:
        results['influencer'] = str(e)

    try:
        from app.modules.realtime import monitor_keywords
        r = monitor_keywords(posts, case.keyword)
        save_result(case_id, 'realtime', r)
        results['realtime'] = 'ok'
    except Exception as e:
        results['realtime'] = str(e)

    try:
        from app.modules.competitor import analyze_competitors
        r = analyze_competitors(posts, case.keyword)
        save_result(case_id, 'competitor', r)
        results['competitor'] = 'ok'
    except Exception as e:
        results['competitor'] = str(e)

    try:
        from app.modules.prediction import predict_popularity
        r = predict_popularity(posts)
        save_result(case_id, 'prediction', r)
        results['prediction'] = 'ok'
    except Exception as e:
        results['prediction'] = str(e)

    case.status = 'analyzed'
    db.session.commit()
    return jsonify({'success': True, 'modules': results})

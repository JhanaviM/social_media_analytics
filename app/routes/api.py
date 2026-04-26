from flask import Blueprint, jsonify, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Case, RawPost, AnalysisResult
import json

api = Blueprint('api', __name__)


def get_case_posts(case_id):
    case = Case.query.filter_by(id=case_id, user_id=current_user.id).first_or_404()
    posts = RawPost.query.filter_by(case_id=case_id).all()
    return case, [p.to_dict() for p in posts]


def save_result(case_id, module, data):
    existing = AnalysisResult.query.filter_by(case_id=case_id, module=module).first()
    if existing:
        existing.set_data(data)
    else:
        r = AnalysisResult(case_id=case_id, module=module)
        r.set_data(data)
        db.session.add(r)
    db.session.commit()


# ── Module 1: Sentiment Analysis ──────────────────────────────────────────────
@api.route('/sentiment/<int:case_id>', methods=['POST'])
@login_required
def sentiment(case_id):
    case, posts = get_case_posts(case_id)
    if not posts:
        return jsonify({'error': 'No posts found. Load data first.'}), 400
    from app.modules.sentiment import analyze_sentiment
    result = analyze_sentiment(posts)
    save_result(case_id, 'sentiment', result)
    return jsonify(result)


# ── Module 2: Trending Topics ─────────────────────────────────────────────────
@api.route('/trending/<int:case_id>', methods=['POST'])
@login_required
def trending(case_id):
    case, posts = get_case_posts(case_id)
    if not posts:
        return jsonify({'error': 'No posts found.'}), 400
    from app.modules.trending import detect_trends
    result = detect_trends(posts)
    save_result(case_id, 'trending', result)
    return jsonify(result)


# ── Module 3: Network Analysis ────────────────────────────────────────────────
@api.route('/network/<int:case_id>', methods=['POST'])
@login_required
def network(case_id):
    case, posts = get_case_posts(case_id)
    if not posts:
        return jsonify({'error': 'No posts found.'}), 400
    from app.modules.network import analyze_network
    result = analyze_network(posts)
    save_result(case_id, 'network', result)
    return jsonify(result)


# ── Module 4: Recommendation ──────────────────────────────────────────────────
@api.route('/recommendation/<int:case_id>', methods=['POST'])
@login_required
def recommendation(case_id):
    case, posts = get_case_posts(case_id)
    if not posts:
        return jsonify({'error': 'No posts found.'}), 400
    from app.modules.recommendation import get_recommendations
    result = get_recommendations(posts, case.keyword)
    save_result(case_id, 'recommendation', result)
    return jsonify(result)


# ── Module 5: Fake News Detection ────────────────────────────────────────────
@api.route('/fakenews/<int:case_id>', methods=['POST'])
@login_required
def fakenews(case_id):
    case, posts = get_case_posts(case_id)
    if not posts:
        return jsonify({'error': 'No posts found.'}), 400
    from app.modules.fake_news import detect_fake_news
    result = detect_fake_news(posts)
    save_result(case_id, 'fakenews', result)
    return jsonify(result)


# ── Module 6: User Segmentation ──────────────────────────────────────────────
@api.route('/segmentation/<int:case_id>', methods=['POST'])
@login_required
def segmentation(case_id):
    case, posts = get_case_posts(case_id)
    if not posts:
        return jsonify({'error': 'No posts found.'}), 400
    from app.modules.segmentation import segment_users
    result = segment_users(posts)
    save_result(case_id, 'segmentation', result)
    return jsonify(result)


# ── Module 7: Data Visualization ─────────────────────────────────────────────
@api.route('/visualization/<int:case_id>', methods=['POST'])
@login_required
def visualization(case_id):
    case, posts = get_case_posts(case_id)
    if not posts:
        return jsonify({'error': 'No posts found.'}), 400
    from app.modules.visualization import build_charts
    result = build_charts(posts)
    save_result(case_id, 'visualization', result)
    return jsonify(result)


# ── Module 8: Ad Campaign Optimization ───────────────────────────────────────
@api.route('/ads/<int:case_id>', methods=['POST'])
@login_required
def ads(case_id):
    case, posts = get_case_posts(case_id)
    if not posts:
        return jsonify({'error': 'No posts found.'}), 400
    from app.modules.ads import optimize_ads
    result = optimize_ads(posts)
    save_result(case_id, 'ads', result)
    return jsonify(result)


# ── Module 9: Influencer Detection ───────────────────────────────────────────
@api.route('/influencer/<int:case_id>', methods=['POST'])
@login_required
def influencer(case_id):
    case, posts = get_case_posts(case_id)
    if not posts:
        return jsonify({'error': 'No posts found.'}), 400
    from app.modules.influencer import detect_influencers
    result = detect_influencers(posts)
    save_result(case_id, 'influencer', result)
    return jsonify(result)


# ── Module 10: Real-Time Monitoring ──────────────────────────────────────────
@api.route('/realtime/<int:case_id>', methods=['POST'])
@login_required
def realtime(case_id):
    case, posts = get_case_posts(case_id)
    from app.modules.realtime import monitor_keywords
    result = monitor_keywords(posts, case.keyword)
    save_result(case_id, 'realtime', result)
    return jsonify(result)


# ── Module 11: Competitor Analysis ───────────────────────────────────────────
@api.route('/competitor/<int:case_id>', methods=['POST'])
@login_required
def competitor(case_id):
    case, posts = get_case_posts(case_id)
    if not posts:
        return jsonify({'error': 'No posts found.'}), 400
    from app.modules.competitor import analyze_competitors
    result = analyze_competitors(posts, case.keyword)
    save_result(case_id, 'competitor', result)
    return jsonify(result)


# ── Module 12: Popularity Prediction ─────────────────────────────────────────
@api.route('/prediction/<int:case_id>', methods=['POST'])
@login_required
def prediction(case_id):
    case, posts = get_case_posts(case_id)
    if not posts:
        return jsonify({'error': 'No posts found.'}), 400
    from app.modules.prediction import predict_popularity
    result = predict_popularity(posts)
    save_result(case_id, 'prediction', result)
    return jsonify(result)


# ── Apify Data Collection ─────────────────────────────────────────────────────
@api.route('/collect/<int:case_id>', methods=['POST'])
@login_required
def collect_data(case_id):
    case = Case.query.filter_by(id=case_id, user_id=current_user.id).first_or_404()
    token = current_app.config.get('APIFY_API_TOKEN', '')
    if not token:
        return jsonify({'error': 'No Apify token configured.'}), 400
    from app.modules.data_loader import collect_from_apify
    try:
        posts, count = collect_from_apify(token, case.keyword, case.platform, max_items=100)
        RawPost.query.filter_by(case_id=case_id).delete()
        db.session.commit()
        for p in posts:
            rp = RawPost(case_id=case_id, **p)
            db.session.add(rp)
        case.status = 'data_loaded'
        db.session.commit()
        return jsonify({'success': True, 'count': count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Report Generation ─────────────────────────────────────────────────────────
@api.route('/report/<int:case_id>', methods=['GET'])
@login_required
def generate_report(case_id):
    case = Case.query.filter_by(id=case_id, user_id=current_user.id).first_or_404()
    results = {r.module: r.get_data() for r in AnalysisResult.query.filter_by(case_id=case_id).all()}
    from app.modules.report import generate_pdf_report
    pdf_path = generate_pdf_report(case, results)
    from flask import send_file
    return send_file(pdf_path, as_attachment=True, download_name=f'{case.name}_report.pdf')


# ── Run All Modules ───────────────────────────────────────────────────────────
@api.route('/run-all/<int:case_id>', methods=['POST'])
@login_required
def run_all(case_id):
    case, posts = get_case_posts(case_id)
    if not posts:
        return jsonify({'error': 'No posts found. Load data first.'}), 400

    results = {}
    modules = [
        ('sentiment', 'app.modules.sentiment', 'analyze_sentiment', [posts]),
        ('trending', 'app.modules.trending', 'detect_trends', [posts]),
        ('network', 'app.modules.network', 'analyze_network', [posts]),
        ('recommendation', 'app.modules.recommendation', 'get_recommendations', [posts, case.keyword]),
        ('fakenews', 'app.modules.fake_news', 'detect_fake_news', [posts]),
        ('segmentation', 'app.modules.segmentation', 'segment_users', [posts]),
        ('visualization', 'app.modules.visualization', 'build_charts', [posts]),
        ('ads', 'app.modules.ads', 'optimize_ads', [posts]),
        ('influencer', 'app.modules.influencer', 'detect_influencers', [posts]),
        ('realtime', 'app.modules.realtime', 'monitor_keywords', [posts, case.keyword]),
        ('competitor', 'app.modules.competitor', 'analyze_competitors', [posts, case.keyword]),
        ('prediction', 'app.modules.prediction', 'predict_popularity', [posts]),
    ]
    for module_key, module_path, func_name, args in modules:
        try:
            import importlib
            mod = importlib.import_module(module_path)
            fn = getattr(mod, func_name)
            result = fn(*args)
            save_result(case_id, module_key, result)
            results[module_key] = 'success'
        except Exception as e:
            results[module_key] = f'error: {str(e)}'

    case.status = 'analyzed'
    db.session.commit()
    return jsonify({'success': True, 'modules': results})

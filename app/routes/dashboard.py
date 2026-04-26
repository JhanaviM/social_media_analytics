from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Case, AnalysisResult

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/')
@login_required
def index():
    cases = Case.query.filter_by(user_id=current_user.id).order_by(Case.created_at.desc()).all()
    total_posts = 0
    for c in cases:
        from app.models import RawPost
        total_posts += RawPost.query.filter_by(case_id=c.id).count()
    stats = {
        'total_cases': len(cases),
        'total_posts': total_posts,
        'total_analyses': AnalysisResult.query.join(Case).filter(Case.user_id == current_user.id).count()
    }
    return render_template('dashboard/index.html', cases=cases, stats=stats)


@dashboard.route('/case/<int:case_id>')
@login_required
def case_detail(case_id):
    case = Case.query.filter_by(id=case_id, user_id=current_user.id).first_or_404()
    from app.models import RawPost
    posts = RawPost.query.filter_by(case_id=case_id).all()
    results = {r.module: r.get_data() for r in AnalysisResult.query.filter_by(case_id=case_id).all()}
    return render_template('dashboard/case_detail.html', case=case, posts=posts, results=results)

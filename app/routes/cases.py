from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Case, RawPost
from datetime import datetime

cases = Blueprint('cases', __name__)


@cases.route('/new', methods=['GET', 'POST'])
@login_required
def new_case():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        keyword = request.form.get('keyword', '').strip()
        platform = request.form.get('platform', 'X')
        description = request.form.get('description', '')
        apify_source = request.form.get('apify_source', '')
        post_ids = request.form.get('post_ids', '')

        if not name or not keyword:
            flash('Name and keyword are required.', 'danger')
            return render_template('cases/new_case.html')

        case = Case(
            name=name,
            keyword=keyword,
            platform=platform,
            description=description,
            apify_source=apify_source,
            post_ids=post_ids,
            user_id=current_user.id
        )
        db.session.add(case)
        db.session.commit()
        flash(f'Case "{name}" created successfully!', 'success')
        return redirect(url_for('dashboard.case_detail', case_id=case.id))

    return render_template('cases/new_case.html')


@cases.route('/<int:case_id>/delete', methods=['POST'])
@login_required
def delete_case(case_id):
    case = Case.query.filter_by(id=case_id, user_id=current_user.id).first_or_404()
    db.session.delete(case)
    db.session.commit()
    flash('Case deleted.', 'info')
    return redirect(url_for('dashboard.index'))


@cases.route('/<int:case_id>/load-sample', methods=['POST'])
@login_required
def load_sample(case_id):
    """Load built-in sample data for demo/testing."""
    case = Case.query.filter_by(id=case_id, user_id=current_user.id).first_or_404()
    from app.modules.data_loader import generate_sample_posts
    RawPost.query.filter_by(case_id=case_id).delete()
    db.session.commit()
    posts = generate_sample_posts(case.keyword, case.platform, count=100)
    for p in posts:
        rp = RawPost(case_id=case_id, **p)
        db.session.add(rp)
    case.status = 'data_loaded'
    db.session.commit()
    flash(f'Loaded {len(posts)} sample posts for "{case.keyword}".', 'success')
    return redirect(url_for('dashboard.case_detail', case_id=case_id))

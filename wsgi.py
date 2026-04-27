"""
WSGI entry point for production deployment.
Gunicorn calls: wsgi:app
"""
import os
from app import create_app, db
from app.models import User

app = create_app()


def init_db():
    """Create tables and seed default admin on first boot."""
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            from flask_bcrypt import Bcrypt
            bcrypt = Bcrypt(app)
            admin = User(
                username='admin',
                email='admin@sma.com',
                password=bcrypt.generate_password_hash('admin123').decode('utf-8'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created: admin / admin123")


# Run DB init every startup (idempotent — skips if already done)
init_db()


if __name__ == '__main__':
    app.run()

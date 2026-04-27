import os
from app import create_app, db
from app.models import User

app = create_app()

def init_db():
    with app.app_context():
        db.create_all()
        try:
            existing = User.query.filter_by(username='admin').first()
            if not existing:
                from flask_bcrypt import Bcrypt
                b = Bcrypt(app)
                admin = User(
                    username='admin',
                    email='admin@sma.com',
                    password=b.generate_password_hash('admin123').decode('utf-8'),
                    is_admin=True
                )
                db.session.add(admin)
                db.session.commit()
                print("Admin user created: admin / admin123")
        except Exception as e:
            print(f"DB init warning: {e}")

init_db()

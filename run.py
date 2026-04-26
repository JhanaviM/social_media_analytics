from app import create_app, db
from app.models import User, Case, AnalysisResult

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Case': Case, 'AnalysisResult': AnalysisResult}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create default admin user if not exists
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
            print("Default admin user created: admin / admin123")
    app.run(debug=True, host='0.0.0.0', port=5000)

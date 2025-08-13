
import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///data/subscriptions.db')

    # Ensure data folder exists
    os.makedirs(os.path.join(app.root_path, 'data'), exist_ok=True)

    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return 'Subscription Manager Home Page'

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

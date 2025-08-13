import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # secret key (needed by Flask even if you don't use sessions yet)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')

    # ==== ABSOLUTE, SAFE SQLITE PATH (works on Render) ====
    db_dir = os.path.join(app.root_path, 'data')
    os.makedirs(db_dir, exist_ok=True)  # make sure folder exists BEFORE engine init
    db_file = os.path.join(db_dir, 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file}"

    # recommended settings
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "connect_args": {"check_same_thread": False}
    }

    # init DB + migrations
    db.init_app(app)
    Migrate(app, db)

    # create tables on first boot
    with app.app_context():
        db.create_all()

    # simple test route
    @app.route("/")
    def index():
        return "Subscription Manager Home Page"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

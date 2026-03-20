import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

# создаём экземпляры один раз
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', f"sqlite:///{os.path.join(basedir, 'tasks.db')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)

    # импорт моделей и Blueprint-ов только после init_app
    from app.models import User
    from app.auth.routes import auth_bp
    from app.tasks.routes import task_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))

    # создаём таблицы SQLite внутри контекста приложения
    with app.app_context():
        db.create_all()

    return app

app = create_app()
if __name__ == '__main__':
    # app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)

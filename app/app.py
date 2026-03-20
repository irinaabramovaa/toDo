from flask import Flask, redirect, url_for
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from app.models import User, db
from app.auth.routes import auth_bp
from app.tasks.routes import task_bp

# Загружаем переменные окружения из .env (для локальной разработки)
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Конфигурация
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'sqlite:///tasks.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Инициализация базы данных
    db.init_app(app)
    Migrate(app, db)

    # Настройка LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Регистрация Blueprint'ов
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))

    return app

# Создаём приложение
app = create_app()

# Для локальной разработки (не используется на Render)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

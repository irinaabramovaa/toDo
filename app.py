import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from flask_login import LoginManager, login_required, current_user
import os
from dotenv import load_dotenv
from models import User, Task, db
from auth import auth_bp
from tasks import task_bp



# из .env загружаем переменные для доступа к бд
load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()  # ← Создаём экземпляр
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('auth.login'))



if __name__ == '__main__':
    # app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
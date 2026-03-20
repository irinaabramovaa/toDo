from flask import Blueprint

task_bp = Blueprint('task', __name__, url_prefix='/task')

from . import routes  # Импортируем маршруты

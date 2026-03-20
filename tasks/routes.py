from flask import request, redirect, url_for, flash
from models import db, Task
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for
from . import task_bp

@task_bp.route('/')
@login_required
def index():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', tasks=tasks)
@task_bp.route('/add', methods=['POST'])
def add_task():
    task = Task(user_id=current_user.id,title=request.form['title'], done=False)
    if task:
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('task.index'))

@task_bp.route('/<int:task_id>/toggle', methods=['POST'])
@login_required
def toggle_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    task.done = not task.done
    db.session.commit()
    flash('Статус изменён!', 'success')
    return redirect(url_for('task.index'))

@task_bp.route('/<int:task_id>/edit', methods=['POST'])
@login_required
def edit_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    new_title = request.form.get('title', '').strip()
    if new_title:
        task.title = new_title
        db.session.commit()
        flash('Задача обновлена!', 'success')
    return redirect(url_for('task.index'))

@task_bp.route('/<int:task_id>/delete', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash('Задача удалена!', 'success')
    return redirect(url_for('task.index'))
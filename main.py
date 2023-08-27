from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from __init__ import create_app
from __init__ import db
from datetime import datetime
from models import File
from flask_login import login_required, current_user
from functions import *
import os

indexx = 0
main = Blueprint('main', __name__, static_folder="static")
uploads = 'uploads'


@main.route('/profile/', methods=['GET'])
@login_required
def profile():
    return profile


@main.route('/index/', methods=['GET'])
@login_required
def index():
    return render_template('index.html', name=current_user.name)


@main.route('/upload/', methods=['GET', 'POST'])
@login_required
def upload_file():
    global indexx
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            if file:
                filename = os.path.join(uploads,
                                        file.filename.split('.')[0] + str(indexx) + '.' + file.filename.split('.')[1])
                file.save(filename)
                file_save_db = File(email=current_user.email,
                                    file_path=file.filename.split('.')[0] + str(indexx) + '.' +
                                              file.filename.split('.')[1],
                                    date=datetime.utcnow().strftime('%m.%d.%Y %H:%M:%S'))
                db.session.add(file_save_db)
                db.session.commit()
                indexx += 1
        flash('File uploaded successfully')
    return render_template('get_file.html')


@main.route('/list_files/', methods=['GET'])
@login_required
def get_files():
    list_files = os.listdir(uploads)
    my_files = []
    files = File.query.all()
    for file in files:
        if file.email == current_user.email:
            my_files.append({'path': file.file_path, 'id': file.id})
    return render_template('list_files.html', list_files=list_files, my_files=my_files)


@main.route('/delete_file/<int:id>', methods=['GET'])
@login_required
def delete_file(id):
    file = File.query.get_or_404(id)
    if file.email == current_user.email:
        db.session.delete(file)
        db.session.commit()
        filename = os.path.join(uploads, file.file_path)
        os.remove(filename)
        flash(f'success deleted {file.file_path}')
        return redirect(url_for('main.get_files'))
    else:
        return 'access_denied'
    return render_template('main.get_files')


@main.route('/details/<string:filename>', methods=['GET', 'POST'])
@login_required
def details(filename):
    page = request.args.get('page', type=int, default=1)
    items_per_page = 50
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    path = os.path.join(uploads, filename)
    file_extens = filename.split('.')[1]
    filters = None
    sort_columns = None
    data = None
    if request.method == 'POST':
        filters = request.form.get('filter')
        sort_columns = request.form.get('sort')
        data = get_csv(path, filters, sort_columns, file_extens)
    elif request.method == 'GET':
        data = get_csv(path, filters, sort_columns, file_extens)
    if data[3] != False:
        flash('Файл не поддерживается')
        data = None
    else:
        if data[1] == True:
            flash('Ничего не найдено')
            data = None
        else:
            if data[2] != None:
                found_lines = data[2]
                flash(found_lines)
        data = data[0].iloc[start_index:end_index].to_dict(orient='records')

    return render_template('show_data.html', page=page, filename=filename, data=data)


with create_app().app_context():
    db.create_all()
if __name__ == "main":
    create_app().run()

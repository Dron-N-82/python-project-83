# import psycopg2
# from psycopg2.extras import RealDictCursor
import os
import requests
from flask import Flask, render_template, \
    request, flash, get_flashed_messages, \
    redirect, url_for
from urllib.parse import urlparse
from dotenv import load_dotenv
from validators import url
from page_analyzer.parser import get_data
from page_analyzer.db import UrlRepository
from page_analyzer.validator import normalization


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
# conn = psycopg2.connect(DATABASE_URL)


@app.route("/")
def index():
#    if conn:
#        return "SQL подключение выполнено"
    app.logger.info("Получен запрос к главной странице")
    value = ''
    return render_template('index.html', value=value), 200

@app.route("/urls")
def urls_get():
    repo = UrlRepository(DATABASE_URL)
    all_urls = repo.get_all_list_urls()

    return render_template('list_urls.html', urls=all_urls)

@app.route("/urls", methods=['POST'])
def add_url():
    name = request.form.get('url')
    # urls = urlparse(name)
    # norm_url = f'{urls.scheme}://{urls.netloc}'

    norm_url = normalization(name)
    
    repo = UrlRepository(DATABASE_URL)

    if url(name): # Проверка на валидность
        app.logger.info("Добавляем ссылку в БД")
        try:
            data = repo.check_id(norm_url)
            if data: # если запись в БД существует
                app.logger.info("Такая ссылка уже есть в базе.")
                flash('URL уже существует', 'info')
            else: # если записи в БД нет
                data = repo.ins_url(norm_url)
                app.logger.info("Cсылка успешно добавлна в БД")
                flash('URL успешно добавлен', 'success')
        except Exception as e:
            app.logger.error(f"Произошла ошибка при добавлении ссылки: {e}")
    else:
        app.logger.info('Некорректный URL')
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages, value=name), 422
    return redirect(url_for('show_url', id=data['id']), code=302)

@app.route("/urls/<id>")
def show_url(id):
    repo = UrlRepository(DATABASE_URL)
    messages = get_flashed_messages(with_categories=True)

    url_data = repo.find_id_url(id)
    check_data = repo.sel_checks_url(id)

    return render_template(
        'show.html',
        url_data=url_data,
        check_data=check_data,
        messages=messages,
    )

@app.route("/urls/<id>/checks", methods=['POST'])
def add_check_url(id):
    repo = UrlRepository(DATABASE_URL)
    url_info = repo.find_id_url(id)

    try:
        response = requests.get(url_info['name'], timeout=1.5)
        response.raise_for_status()
    except requests.RequestException as e:
        app.logger.error(f"Произошла ошибка при проверке: {e}")
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url', id=id))

    sc = requests.get(url_info['name']).status_code
    row = get_data(response)
    row['status'] = sc
    
    if row['h1'] is None:
        row['h1'] = ''
    if row['title'] is None:
        row['title'] = ''
    if row['description'] is not None and len(row['description']) > 250:
        row['description'] = f"{row['description'][:189]}..."
    elif row['description'] is None:
        row['description'] = ''

    repo.ins_check_url(url_info, row)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for (
                                'show_url',
                                id=id,
                            ),
                            code=302)

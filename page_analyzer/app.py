import psycopg2
#from psycopg2.extras import RealDictCursor
import os
import requests
from flask import Flask, render_template, \
    request, flash, get_flashed_messages, \
    redirect, url_for
from urllib.parse import urlparse
from dotenv import load_dotenv
from validators import url

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)


@app.route("/")
def index():
#    if conn:
#        return "SQL подключение выполнено"
    app.logger.info("Получен запрос к главной странице")
    value = ''
    return render_template('index.html', value=value), 200

@app.route("/urls")
def urls_get():

    sql = """
        SELECT *
        FROM (
            SELECT DISTINCT ON (u.id)
                u.id,
                u.name,
                uc.created_at AS check_date,
                uc.status_code
            FROM urls u
            LEFT JOIN url_checks uc ON uc.url_id = u.id
            ORDER BY u.id, uc.created_at DESC
        ) sub
        ORDER BY sub.id DESC;
        """        
    with conn.cursor() as curs:
        curs.execute(sql)
        all_urls = curs.fetchall()
#        print(all_urls)
#        for row in all_urls:
#            print(row)
#            if row[2] is None:
#                row[2] = ''
#            if row[3] is None:
#                row[3] = ''

    return render_template('list_urls.html', urls=all_urls)

@app.route("/urls", methods=['POST'])
def add_url():
    name = request.form.get('url')
    urls = urlparse(name)

    norm_url = f'{urls.scheme}://{urls.netloc}'

    sql_check = "SELECT id FROM urls WHERE name = %s"
    sql_ins = "INSERT INTO urls (name) VALUES (%s)"
    
    if url(name): # Проверка на валидность
        app.logger.info("Добавляем ссылку в БД")
        try:
            with conn:
                with conn.cursor() as curs:
                    # Проверка существования записи
                    curs.execute(sql_check, (norm_url,))
                    data = curs.fetchone()
                    if data: # если запись в БД существует
                        app.logger.info("Такая ссылка уже есть в базе.")
                        flash('URL уже существует', 'info')
                    else: # если записи в БД нет
                        curs.execute(sql_ins, (norm_url,))
                        app.logger.info("Cсылка успешно добавлна в БД")
                        curs.execute(sql_check, (norm_url,))
                        data = curs.fetchone()
                        flash('URL успешно добавлен', 'success')
        except Exception as e:
            app.logger.error(f"Произошла ошибка при добавлении ссылки: {e}")
    else:
        app.logger.info('Некорректный URL')
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages, value=name), 422
    return redirect(url_for('show_url', id=data[0]), code=302)

@app.route("/urls/<id>")
def show_url(id):
    messages = get_flashed_messages(with_categories=True)
    sql = """SELECT id,
                name,
                TO_CHAR(created_at, 'YYYY-MM-DD') AS date
                FROM urls WHERE  id = %s"""
    sql_ch = """SELECT id, status_code, created_at
                FROM url_checks WHERE  url_id = %s
                ORDER BY created_at DESC"""
    with conn:
        with conn.cursor() as curs:
            curs.execute(sql, (id,))
            data = curs.fetchone()
            curs.execute(sql_ch, (id,))
            check_data = curs.fetchall()
    return render_template(
        'show.html',
        id=data[0],
        name=data[1],
        date=data[2],
        check_data=check_data,
        messages=messages,
    )

@app.route("/urls/<id>/checks", methods=['POST'])
def add_check_url(id):
    sql_ins = """INSERT INTO url_checks (url_id,
                                        status_code,
                                        h1, title,
                                        description)
                VALUES (%s, %s, %s, %s, %s)
                """
    sql_find = """
                SELECT *
                FROM urls WHERE id = %s
                """
    with conn.cursor() as curs:
            curs.execute(sql_find, (id,))
            url_info = curs.fetchone()

    try:
        response = requests.get(url_info[1], timeout=1.5)
        response.raise_for_status()
    except requests.RequestException as e:
        app.logger.error(f"Произошла ошибка при проверке: {e}")
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url', id=id))

    with conn:
        with conn.cursor() as curs:
#            curs.execute(sql_find, (id,))
#            url_info = curs.fetchone()
#            print(url_info)
            sc = requests.get(url_info[1]).status_code
            curs.execute(sql_ins, (id, sc, '', '', '',))

    flash('Страница успешно проверена', 'success')
    return redirect(url_for (
                                'show_url',
                                id=id,
                                sc=sc,
                            ),
                            code=302)

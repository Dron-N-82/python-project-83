import psycopg2
#from psycopg2.extras import RealDictCursor
import os
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

'''
@app.route("/")
def hello():
    return "Welcome to Flask!"
'''

@app.route("/")
def index():
#    if conn:
#        return "SQL подключение выполнено"
    app.logger.info("Получен запрос к главной странице")
    value = ''
#    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', value=value), 200


@app.route("/urls")
def urls_get():
    sql = "SELECT id, name FROM urls ORDER BY id DESC"
#    with conn.cursor(cursor_factory=RealDictCursor) as curs:
    with conn.cursor() as curs:
        curs.execute(sql)
        all_urls = curs.fetchall()
#        print(all_urls)
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
#        return redirect(url_for('index'), code=302)
#    print(data[0])
#    print(data[1])
#    return render_template('show.html'), 200
    
    return redirect(url_for('show_url', id=data[0]), code=302)

@app.route("/urls/<id>")
def show_url(id):
    messages = get_flashed_messages(with_categories=True)
    sql = """SELECT id,
                name,
                TO_CHAR(created_at, 'YYYY-MM-DD') AS date
                FROM urls WHERE  id = %s"""
    with conn:
        with conn.cursor() as curs:
            curs.execute(sql, (id,))
            data = curs.fetchone()
#            name = curs.fetchone()[1]
#            date = curs.fetchone()[2]
    return render_template(
        'show.html',
        id=data[0],
        name=data[1],
        date=data[2],
        messages=messages,
    )


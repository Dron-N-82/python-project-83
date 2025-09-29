import psycopg2
from psycopg2.extras import RealDictCursor


class DatabaseConnection:
    def __init__(self, database_url):
        self.database_url = database_url

    def __enter__(self):
        self.conn = psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
        self.cur = self.conn.cursor()
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cur.close()
        self.conn.close()


class UrlRepository:
    def __init__(self, database_url):
        self.cursor = DatabaseConnection(database_url)

    # Вывод полного списка сайтов
    def get_all_list_urls(self):
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
        with self.cursor as curs:
            curs.execute(sql)
            all_urls = curs.fetchall()

            for row in all_urls:
                if row['check_date'] is None:
                    row['check_date'] = ''
                if row['status_code'] is None:
                    row['status_code'] = ''

            return all_urls

    # Проверка существования записи в таблце urls
    def check_id(self, norm_url):
        sql_check = "SELECT id FROM urls WHERE name = %s;"
        with self.cursor as curs:
            curs.execute(sql_check, (norm_url,))
            id_ch = curs.fetchone()

            return id_ch
    
    # Добавление адреса сайта в таблицу urls
    def ins_url(self, norm_url):
        sql_ins = "INSERT INTO urls (name) VALUES (%s) RETURNING id"
        # print(f'db.py 66 {norm_url}')
        with self.cursor as curs:
            # print(f'db.py 68 {norm_url}')
            curs.execute(sql_ins, (norm_url,))
            id_ins = curs.fetchone()
            # print(f'db.py 71 {id_ins}')
            return id_ins

    # Выбор строки из таблцы urls по id
    def find_id_url(self, id):
        sql_find = "SELECT * FROM urls WHERE  id = %s"
        with self.cursor as curs:
            curs.execute(sql_find, (id,))
            url_data = curs.fetchone()

            return url_data

    # Добавление проверки в таблицу url_checks
    def ins_check_url(self, url_info, row):
        sql_ins = """INSERT INTO url_checks (url_id,
                                        status_code,
                                        h1, title,
                                        description)
                VALUES (%s, %s, %s, %s, %s)
                """
        with self.cursor as curs:
            curs.execute(sql_ins, (
                                url_info['id'],
                                row['status'],
                                row['h1'],
                                row['title'],
                                row['description'],
                                )
                        )

    #  Выбор проверок из таблицы url_checks
    def sel_checks_url(self, id):
        sql_ch = """SELECT id, status_code, h1, title, description, created_at
                FROM url_checks WHERE  url_id = %s
                ORDER BY id DESC"""
        with self.cursor as curs:
            curs.execute(sql_ch, (id,))
            check_data = curs.fetchall()
            
            return check_data
### Hexlet tests and SonarQube:
[![Actions Status](https://github.com/Dron-N-82/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Dron-N-82/python-project-83/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Dron-N-82_python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Dron-N-82_python-project-83)

# Page Analyzer

## Описание
Page Analyzer – это сайт, который анализирует указанные страницы на SEO-пригодность по аналогии с [PageSpeed Insights](https://pagespeed.web.dev/)

### Демонстрационный проект:
https://python-project-83-ht8g.onrender.com

### Инструменты и описание:

[uv](https://docs.astral.sh/uv/) — быстрый пакет Python и менеджер проектов

[ruff](https://docs.astral.sh/ruff/) — линтер

[Flask](https://flask.palletsprojects.com/en/stable/) — фреймворк для создания веб-приложений на языке программирования Python

[Gunicorn](https://docs.gunicorn.org/en/latest/index.html) — минивеб-сервер, осуществляющий запуск Python-приложения

[python-dotenv](https://pypi.org/project/python-dotenv/) — управление переменными окружения, считывая пары «ключ-значение» из .env файла. Это помогает в разработке приложений, основанных на принципах 12 факторов.

[Bootstrap](https://getbootstrap.com/docs/5.3/getting-started/introduction/) — скомпилированный CSS и JavaScript, это мощный и многофункциональный набор инструментов для фронтенда.

[Psycopg](https://getbootstrap.com/docs/5.3/getting-started/introduction/) — самый популярный адаптер баз данных PostgreSQL для языка программирования Python

[validators](https://validators.readthedocs.io/en/latest/#module-validators.url) — модуль для проверки данных на соответствие критериям в Python

[Requests](https://requests.readthedocs.io/en/latest/) — библиотека для языка Python, осуществляющая работу с HTTP-запросами

[Beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) — библиотека Python, используемая для парсинга HTML и XML документов

## Установка

### Склонировать репозиторий:

```
git clone git@github.com:lyovaparsyan94/python-project-83.git

cd python-project-83
```

### Для хранения конфиденциональной информации создать файл .env в директории page-analyzer 

```
DATABASE_URL = postgresql://{username}{password}@{host}:{port}/{basename}

SECRET_KEY = "{your_secret_key}"
```

### Install
```
make build
```
### Для запуска приложения используй
```
make start
```

# сборка проекта
install:
	uv sync

# старт проекта
dev:
	uv run flask --debug --app page_analyzer:app run --host 0.0.0.0 --port 8088

# запуск приложение в режиме отладки в процессе разработки
PORT ?= 8081
start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

# сборка проекта
build:
	./build.sh

# запуск приложения на render.com
render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

# линтер Ruff
lint:
	uv run ruff check page_analyzer
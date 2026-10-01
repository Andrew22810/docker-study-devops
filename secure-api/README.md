Уровень 1

На первом этапе приложение было упаковано в Docker-образ на основе python:3.11.

Были реализованы:

requirements.txt;

Dockerfile;

.dockerignore;

установка Python-зависимостей;

публикация порта 8080;

запуск приложения через Docker.

Сборка образа:

docker build -t secure-api:v1 .

Запуск:

docker run -d --name secure-api-v1 -p 8080:8080 secure-api:v1

Проверка API:

curl http://localhost:8080/health

Ответ:

{"status":"ok"}

Уровень 2

На втором этапе был реализован multi-stage Docker build.

Builder

На этапе builder устанавливаются:

gcc;

musl-dev;

python3-dev.

После этого зависимости устанавливаются в отдельную директорию:

/install

Runtime

Финальный образ использует:

python:3.11-alpine

В runtime-образ переносятся только необходимые Python-зависимости.

Компиляторы и инструменты сборки в финальный образ не попадают.

Сборка:

docker build -t secure-api:v3 .

Размер финального образа:

около 109 MB

Это меньше установленного требования в 150 MB.

Историю образа можно проверить:

docker history secure-api:v3

Уровень 3

На третьем этапе контейнер был усилен с точки зрения безопасности и эксплуатации.

Non-root

Создан отдельный пользователь:

appuser

Приложение запускается от него:

USER appuser

Проверка:

docker exec secure-api whoami

Результат:

appuser

Read-only filesystem

Контейнер поддерживает запуск с:

--read-only

Для хранения логов используется отдельный Docker volume:

/var/log/app

Путь к директории задаётся через переменную:

LOG_DIR=/var/log/app

Healthcheck

Docker автоматически проверяет endpoint:

/health

Каждые 30 секунд выполняется проверка состояния приложения.

Проверка статуса:

docker inspect --format='{{json .State.Health.Status}}' secure-api

Результат:

"healthy"

Ограничение Linux capabilities

Финальный контейнер запускается с:

--cap-drop ALL

Также используется:

--security-opt no-new-privileges

Graceful shutdown

Приложение запускается через exec-form:

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

Это позволяет Uvicorn получать сигналы ОС непосредственно.

Финальный запуск

Финальный production-ready контейнер запускается командой:

docker run -d --name secure-api -p 8080:8080 --read-only --cap-drop ALL --security-opt no-new-privileges secure-api:v5

Проверка контейнера:

docker ps

Проверка Healthcheck:

docker inspect --format='{{json .State.Health.Status}}' secure-api

Ожидаемый результат:

"healthy"

Проверка API:

curl http://localhost:8080/health

Ожидаемый ответ:

{"status":"ok"}

Проверка генерации хэша:

curl "http://localhost:8080/hash?password=hello"

Приложение возвращает bcrypt-хэш переданного пароля.

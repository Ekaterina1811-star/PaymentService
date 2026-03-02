# payment-service

Payment Service

This project was generated with [`wemake-django-template`](https://github.com/wemake-services/wemake-django-template). Current template version is: [55c18b2](https://github.com/wemake-services/wemake-django-template/tree/55c18b2ebcd5b56acd1c1143750c5cd57d2b61ec). See what is [updated](https://github.com/wemake-services/wemake-django-template/compare/55c18b2ebcd5b56acd1c1143750c5cd57d2b61ec...master) since then.


[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake-services.github.io)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![Python](https://img.shields.io/badge/Python-%203.12-blue?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-%205.2-blue?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DjangoRESTFramework-%203.16.1-blue?style=flat-square&logo=django)](https://www.django-rest-framework.org/)
[![Celery](https://img.shields.io/badge/Celery-%205.6.2-blue?style=flat-square&logo=celery)](https://docs.celeryq.dev/en/stable/)
[![Redis](https://img.shields.io/badge/Redis-%206.0.0-blue?style=flat-square&logo=redis)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-%2029.1.5-blue?style=flat-square&logo=docker)](https://www.docker.com/)
[![DockerCompose](https://img.shields.io/badge/Docker_Compose-%205.0.2-blue?style=flat-square&logo=docsdotrs)](https://docs.docker.com/compose/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-%2025.0.2-blue?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![Caddy](https://img.shields.io/badge/Caddy-%20-blue?style=flat-square&logo=caddy)](https://caddyserver.com/)

## Описание
 Удобный сервис, с помощью которого можно создавать денежные сборы и управлять ими

## Функционал

- Управление групповыми денежными сборами;
- Возможность создания, чтения, обновления и удаления сборов и платежей;
- Безопасная аутентификация и авторизация с использованием JWT-токенов;
- Асинхронная обработка задач с помощью Celery для повышения производительности;
- Отправка писем на электронную почту при создании сбора/платежа;
- Реализовано кэширование данных, возвращаемых GET-эндпоинтом;

## Технические особенности
Данная инструкция подразумевает, что на вашем локальном/удалённом сервере
уже установлен Git, Python 3.12, PostgreSQL, poetry, Docker, Docker Compose.
В проекте настроена автодокументация с помощью Swagger.
Для ознакомления перейдите по ссылке http://127.0.0.1/api/swagger/

You will need:

- `python3.12` (see `pyproject.toml` for exact version), use `pyenv install`
- `postgresql` (see `docker-compose.yml` for exact version)
- Latest `docker`

Перед началом разработки нужно обязательно:

+ Установить poetry https://python-poetry.org/docs/#installation
+ Выполнить команду `poetry install` для установки зависимостей
+ Выполнить команду `poetry shell` для активации виртуального окружения

> Можно вносить изменения в файлы с запущенными контейнерами, изменения будут видны сразу потому как папка с исходным кодом замаунтина в контейнер.

С подробными инструкциями запуска вы можете ознакомиться ниже.

***

## Documentation

Full documentation is available here: [`docs/documents/`](docs/documents).

## 🐳 Запуск проекта локально в Docker-контейнерах с помощью Docker Compose
###
Клонировать репозиторий:

```python
git clone https://github.com/Ekaterina1811-star/PaymentService.git
```

Перейти в папку с проектом:

```python
cd payment-service/
```

Создать файл .env в папке config:

```python
cd config
cp .env.template .env
```

В корне проекта находится файл **Makefile**, с помощью которого вы можете
запустить проект локально в Docker контейнерах.

Находясь в **корневой** директории выполните следующую команду:

```shell
make up
```

Она сбилдит Docker образы и запустит backend, СУБД, Redis, Flower
в отдельных Docker контейнерах.

Откройте второй терминал в **корневой** директории и выполните
для применения миграций:

```shell
make makemigrations
make migrate
```


По завершении всех операции проект будет запущен и доступен по адресу
http://127.0.0.1/



Для остановки Docker контейнеров, находясь в **корневой** директории проекта выполните
следующую команду:

```shell
make stop
```

## Загрузка тестовых данных

В проекте предусмотрена генерация тестовых данных в БД.
Для заполнения БД тестовыми данными, можно выполнить:
```shell
make create-test-data
```

> С дополнительными командами вы можете ознакомиться в файле **Makefile.**

***

## Автор

[**Екатерина Старунская**](https://github.com/Ekaterina1811-star)



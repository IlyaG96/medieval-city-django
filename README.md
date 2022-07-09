# Проект Medieval City (Django)

## Что умеет приложение? 

Приложение состоит из нескольких составляющих:
- Главная страница - резюме.
- Страницы регистрации и логинизации.
- Страница с иерархией базы данных населения средневекового города (только для авторизированных пользователей).
- Страница редактирования информации о жителе города. (только для авторизированных пользователей).
- Админка (только для персонала и суперпользователей).

## Требования
Создайте в директории medieval-city-django две переменных окружения:
1) `.env` - обязательная.

- `DEBUG`= настройка Django для включения отладочного режима. Принимает значения `TRUE` или `FALSE`. [Документация Django](https://docs.djangoproject.com/en/3.2/ref/settings/#std:setting-DEBUG).
- `SECRET_KEY`= обязательная секретная настройка Django. Это соль для генерации хэшей. Значение может быть любым, важно лишь, чтобы оно никому не было известно. [Документация Django](https://docs.djangoproject.com/en/3.2/ref/settings/#secret-key).
- `ALLOWED_HOSTS`= настройка Django со списком разрешённых адресов. Если запрос прилетит на другой адрес, то сайт ответит ошибкой 400. Можно перечислить несколько адресов через запятую, например `127.0.0.1,192.168.0.1,site.test`. [Документация Django](https://docs.djangoproject.com/en/3.2/ref/settings/#allowed-hosts).
- `DATABASE_URL`= адрес для подключения к базе данных PostgreSQL. Другие СУБД сайт не поддерживает. [Формат записи](https://github.com/jacobian/dj-database-url#url-schema).
- `CSRF_COOKIE_DOMAIN`= `http://127.0.0.1:1337`, `http://mydomain.ru`, `https://mydomain.ru` [Документация](https://docs.djangoproject.com/en/4.0/ref/settings/#csrf-cookie-domain).
- `CSRF_TRUSTED_ORIGINS`= `127.0.0.1:1337`, `mydomain.ru`, [Документация](https://docs.djangoproject.com/en/4.0/ref/settings/#csrf-trusted-origins).


2) `.env.db` - обязательная.

- `POSTGRES_USER`=`psql_user` - если БД должна находиться в контейнере.
- `POSTGRES_PASSWORD`=`psql_pass` - если БД должна находиться в контейнере.
- `POSTGRES_DB`=`psql_db_name` - если БД должна находиться в контейнере.


## Запуск приложения
- Выполните команду:
```shell
docker-compose up --build -d
```
- Загрузить тестовые данные:

```shell
docker-compose exec web python ./manage.py load_data
```
Приложение будет доступно по адресу: [http://127.0.0.1:1337](http://127.0.0.1:1337)


### Завершить работу docker-compose
- Выполните команду:
```shell
docker-compose down -v
```
- `-v` указывается в том случае, если необходимо удалить `volumes`.

### Возможен запуск без использования Docker.

1) Создайте директорию с виртуальным окружением python3.8-3.11 в `директории medieval-city-django`.
2) Активируйте виртуальное окружение, установите все необходимые зависимости.
3) Убедитесь, что postgres запущен и `DATABASE_URL` соответствует URL postgres на Вашем компьютере.
4) В переменной окружения .env установите режим `DEBUG`=`False`.
5) Последовательно выполните команды:
```shell
python3 manage.py migrate
```
```shell
python3 manage.py load_data
```
```shell
python3 manage.py runserver
```

Для очистки базы от тестовых данных выполните команду:
```shell
python3 manage.py flush
```
Приложение будет доступно по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Issues 

Можно улучшить:

- Оптимизировать формы
- Высушить код, исправить его в соотв. с требованиями pep-8 и django best practices.
- Оптимизация скрипта загрузки данных в БД (DRY, annotate и т.д)
- Использование DRF для сериализации данных. Сейчас можно передать неверные параметры в GET запрос и приложение "сломается".
- Переезд на реактивный фронтенд + использование AJAX.
- Спроектировать Масштабируемую структуру БД, которая будет учитывать все возможные требования к проекту.
- Оптимизировать и кастомизировать админ-панель для CRUD операций.
- Вынести данные из load_data в отдельный json-файл

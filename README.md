# Версия для разработки

Нужен python версии 3.x (у меня 3.10).

## Шаги по запуску
Скачать репозиторий
```commandline
git clone ссылка-на-этот-репозиторий
```

Войти в папку проекта, если ещё не в ней:
```commandline
cd dvmn_food
```

Установить зависимости:
```commandline
pip install -r requirements.txt
```

Применить миграции, чтобы создать БД:
```commandline
python manage.py migrate
```

Создать себе пользователя:
```commandline
python manage.py createsuperuser
```

Загрузить начальные данные в базу:
```commandline
python manage.py loaddata recipes.json
```

Запуск
```commandline
python manage.py runserver
```

По умолчанию админка должна быть доступна по адресу http://127.0.0.1:8000/admin/. Пока не добавлял наши сущности в админку.

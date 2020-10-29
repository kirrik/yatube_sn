# Yatube Social Network

Социальная сеть с регистрацией, где пользователи могут  публиковать посты сгруппированные по темам, с возможностью оставлять комментарии к постам, а также подпиской на интересных авторов.

# Для просмотра проекта локально нужно выполнить следующий шаги:

- клонировать репозиторий
- установить виртуальное окружение
```sh
pythom -m venv venv
```
- активировать venv
- установить зависимости проекта
```sh
pip install -r requirements.txt
```
- сделать миграции
```sh
python manage.py migrate
```
для статики скачайте [архив](https://code.s3.yandex.net/backend-developer/learning-materials/static.zip) и распакуйте его в директорию ./posts/static/
- собрать статику
```sh
python manage.py collectstatic
```
- создать суперпользователя (по желанию)
```sh
python manage.py createsuperuser
```
- загрузить данные в БД
```sh
python manage.py loaddata db.json
```
#!/bin/bash

# установка зависимостей
pip install -r requirements.txt

# создание пустой базы данных
#flask --app app.app init-db

# заполнение базы данных тестовыми значениями
#flask --app app.app fill-db

flask --app app.app run -h 0.0.0.0
# YaMDb

Учебный проект Яндекс.Практикум курса Python-разработчик(backend).

## Описание

Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором.

Сами произведения в YaMDb не хранятся, в нём можно поделиться впечатлением.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор. Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

## Установка и запуск в dev-режиме

 1. Установите виртуальное окружение (команда: `python -m venv venv`).
 2. Активируйте виртуальное окружение (команда: `source venv/Scripts/activate`).
 3. Установите зависимости из файла requirements.txt (команда: `pip install -r requirements.txt`).
 4. Заполните базу данных (команда: `python manage.py import_csv`)
 5. Запустите dev-сервер (команда: `python manage.py runserver`).

## Документация к API

 После запуска dev-сервера документация к API доступна по адресу:
 <http://127.0.0.1:8000/redoc/>

## Авторы

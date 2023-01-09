# Домашнее задание по теме "Асинхронность"

Для решения использованы: FastAPI, databases для асинхронных подключений, Postgresql для данных.

---

## Взаимодействие с приложением возможно следующим образом:

1. ### Отправляя GET и POST запросы из Swagger UI FastAPI, Postman, Insomnia и аналогичное.

2. ### Через простой веб-интерфейс

---

## Запуск приложения

1. ### Перед запуском приложения **необходимо подключить базу данных**, сделать это можно в **models.py**, изменив значения переменных с учётными данными. Затем выполнить файл models.py для создания таблиц

2. ### Наполнить таблицы данными можно через **make_fake_tables.py**. Вы можете изменить кол-во магазинов и сделанных продаж через переменные stores_num, sales_num и, при необходимости добавить свои товары в items_list. Затем выполните этот файл, чтобы таблицы наполнились.

3. ### Запустите приложение, выполнив команду **uvicorn main:app --reload**

---

## Взаимодействие через GET и POST

- ### Получить список всех товаров можно отправив get по маршруту /items
- ### Получить список всех магазинов можно отправив get по маршруту /stores
- ### Добавить запись в таблицу о новой продаже можно через post по маршруту /sales **_(данные принимаются и отправляются в json формате, схемы приведены в Swagger Ui по маршруту /docs)_**
- ### Получить ТОП 10 магазинов можно через get по маршруту /top-stores
- ### Получить ТОП 10 товаров можно через get по маршруту /top-items

---

## Через веб-интерфейс

### Доступ можно получить через браузер, зайдя в **_корень сайта '/'_** . Там такие же запросы - ответы, что и через api, просто всё отображается через шаблоны html. С FastAPI до этого не работал, поэтому захотелось попробовать как в нём работают шаблоны.
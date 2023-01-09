import datetime

from faker import Faker
from random import randint
import asyncio
from models import stores, items, sales, database

fake = Faker('Ru-ru')

# Настраиваем параметры наших таблиц
stores_num = 20  # количество магазинов
# список товаров
items_list = {'Iphone 13': 3000, 'Samsung Galaxy': 2000, 'Xiaomi Redmi Note': 1000, 'Nokia 3310': 3500,
              'Iphone 14': 4000, 'SonyEricsson': 5000, 'OnePlus': 2000, 'Realme': 1600, 'Sony': 1400,
              'HP notebook': 3850, 'Macbook PRO': 6182, 'Dell': 2100
              }
sales_num = 50  # количество продаж


# генерируем таблицу с адресами магазинов
async def make_fake_stores(stores_num: int):
    await database.connect()
    for _ in range(stores_num):
        query = stores.insert().values(address=fake.address())
        await database.execute(query)
    await database.disconnect()


asyncio.run(make_fake_stores(stores_num))


# генерируем таблицу с товарами
async def make_fake_items(items_list: dict):
    await database.connect()
    for key, value in items_list.items():
        query = items.insert().values(name=key, price=value)
        await database.execute(query)
    await database.disconnect()


asyncio.run(make_fake_items(items_list))


# генерируем таблицу с продажами
async def make_fake_sales(items_list: dict, sales_num: int, stores_num: int):
    await database.connect()
    for _ in range(sales_num):
        query = sales.insert().values(sale_time=fake.date_time_between(datetime.datetime.now(), '+1y'),
                                      items_id=randint(1, len(items_list)), stores_id=randint(1, stores_num))
        await database.execute(query)
    await database.disconnect()


asyncio.run(make_fake_sales(items_list, sales_num, stores_num))

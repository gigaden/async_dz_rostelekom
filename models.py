import datetime
import databases
from sqlalchemy import Table, MetaData, Column, Integer, VARCHAR, Float, DateTime, ForeignKey, create_engine

# Данные для подключения к БД
DB_USER = "postgres"
DB_NAME = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "127.0.0.1"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

database = databases.Database(DATABASE_URL)

metadata = MetaData()

stores = Table(
    'stores',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('address', VARCHAR)
)

items = Table(
    'items',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', VARCHAR),
    Column('price', Float)
)

sales = Table(
    'sales',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('sale_time', DateTime(), default=datetime.datetime.now(), nullable=False),
    Column('items_id', Integer, ForeignKey('items.id')),
    Column('stores_id', Integer, ForeignKey('stores.id'))
)

engine = create_engine(DATABASE_URL)
metadata.create_all(engine)

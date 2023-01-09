from dateutil.relativedelta import relativedelta
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from html_views.router import router as router_html

from typing import List
from models import database, stores, sales, items
import datetime

from schemas import ItemsOut, StoresOut, SalesIn, SalesOut, TopStoreOut, TopItemsOut

from sqlalchemy import func, select, desc, literal_column

app = FastAPI(
    title='dz_async'
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# выводим все товары
@app.get("/items", response_model=List[ItemsOut], tags=['main'])
async def get_all_items():
    query = items.select()
    return await database.fetch_all(query)


# выводим все магазины
@app.get("/stores", response_model=List[StoresOut], tags=['main'])
async def get_all_stores():
    query = stores.select()
    return await database.fetch_all(query)


# добавляем новую продажу
@app.post("/sales", response_model=SalesOut, tags=['main'])
async def add_new_sales(sale: SalesIn):
    query = sales.insert().values(items_id=sale.id_items, stores_id=sale.id_stores,
                                  sale_time=datetime.datetime.now())
    await database.execute(query)
    return {'items_id': sale.id_items, 'stores_id': sale.id_stores}


# выводим топ товаров по продажам
@app.get('/top-items', response_model=List[TopItemsOut], tags=['main'])
async def get_top_items():
    query = select([items.c.id.label('id'), items.c.name.label('name'),
                    func.count(sales.c.items_id).label('total_items')]
                   ).join(sales, items.c.id == sales.c.items_id).group_by(items.c.id, items.c.name).order_by(
        desc(literal_column('total_items'))
    ).limit(10)
    return await database.fetch_all(query)


# выводим топ 10 магазинов по продажам
@app.get('/top-stores', response_model=List[TopStoreOut], tags=['main'])
async def get_top_stores():
    query = select([stores.c.id.label('id'),
                    stores.c.address.label('address'),
                    func.sum(items.c.price).label('total_sale')]
                   ).join(sales, stores.c.id == sales.c.stores_id).join(
        items, items.c.id == sales.c.items_id).filter(
        stores.c.id == sales.c.stores_id,
        items.c.id == sales.c.items_id,
        sales.c.sale_time >= datetime.date.today() + relativedelta(months=-1)).group_by(stores.c.id,
                                                                                        stores.c.address).order_by(
        desc(literal_column('total_sale'))).limit(10)
    return await database.fetch_all(query)


# пробуем работать через роутер
app.include_router(router_html)

# подключаем шаблоны и статику
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# выводим на главную html шаблон с навигацией
@app.get('/', response_class=HTMLResponse, tags=['html'])
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

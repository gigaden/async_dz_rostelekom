import datetime
from typing import List

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, func, desc, literal_column

from models import sales, stores, items, database
from schemas import TopStoreOut, TopItemsOut

router = APIRouter(
    prefix='/html_views',
    tags=['html']
)

router.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# выводим в html шаблон все магазины из БД
@router.get('/all_stores', response_class=HTMLResponse)
async def return_all_stores(request: Request):
    query = stores.select()
    all_stores = await database.fetch_all(query)
    return templates.TemplateResponse('all_stores.html', {'request': request, 'all_stores': all_stores})


# выводим в html шаблон все товары из БД
@router.get('/all_items', response_class=HTMLResponse)
async def return_all_items(request: Request):
    query = items.select()
    all_items = await database.fetch_all(query)
    return templates.TemplateResponse('all_items.html', {'request': request, 'all_items': all_items})


# выводим страницу с возможностью добавить новую продажу через html форму
@router.get('/make_sale', response_class=HTMLResponse)
async def make_sale(request: Request):
    return templates.TemplateResponse('make_sale.html', {'request': request})


# обрабатываем через форму новую продажу, заносим её в БД и возвращаем страницу с подтверждением
@router.post('/make_sale')
async def make_sale(request: Request, id_stores=Form(), id_items=Form()):
    query = sales.insert().values(items_id=int(id_items), stores_id=int(id_stores),
                                  sale_time=datetime.datetime.now())
    await database.execute(query)
    return templates.TemplateResponse('congratulations.html',
                                      {'request': request, 'id_stores': id_stores, 'id_items': id_items})


# выводим топ 10 магазинов по продажам
@router.get('/top_stores', response_model=List[TopStoreOut], tags=['html'])
async def get_top_stores(request: Request):
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
    top_stores = await database.fetch_all(query)
    return templates.TemplateResponse('top_stores.html',
                                      {'request': request, 'top_stores': top_stores})


# выводим топ товаров по продажам
@router.get('/top_items', response_model=List[TopItemsOut], tags=['html'])
async def get_top_items(request: Request):
    query = select([items.c.id.label('id'), items.c.name.label('name'),
                    func.count(sales.c.items_id).label('total_items')]
                   ).join(sales, items.c.id == sales.c.items_id).group_by(items.c.id, items.c.name).order_by(
        desc(literal_column('total_items'))
    ).limit(10)
    top_items = await database.fetch_all(query)
    return templates.TemplateResponse('top_items.html',
                                      {'request': request, 'top_items': top_items})

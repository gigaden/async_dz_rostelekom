from pydantic import BaseModel


# представление товарных позиций
class ItemsOut(BaseModel):
    id: int
    name: str
    price: float


# представление списка магазинов
class StoresOut(BaseModel):
    id: int
    address: str


# обрабатываем входящую продажу
class SalesIn(BaseModel):
    id_items: int
    id_stores: int


# возвращаем ответ по новой продаже в json
class SalesOut(BaseModel):
    items_id: int
    stores_id: int


# возвращаем ответ по ТОПу магазинов в json
class TopStoreOut(BaseModel):
    id: int
    address: str
    total_sale: float


# возвращае ответ по ТОПу товаров в json
class TopItemsOut(BaseModel):
    id: int
    name: str
    total_items: int

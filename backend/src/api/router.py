import json
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Query, Body
from ..datebase import get_async_session
from .utils import get_all, get_countru, get_item, get_items_countru, get_category, get_items_category, get_items_net_href_, get_net_href
from . import shemas
from fastapi_pagination import Page, paginate

router = APIRouter (
    prefix='/api',
    tags= ['api']
)




@router.get("/get_data")
async def get_data(session: AsyncSession = Depends(get_async_session), 
                   page: int = Query(ge=0, default=0), 
                   size: int = Query(ge=1, default=25)) -> Page[shemas.RawData]:
    
    res = await get_all(session)
    return paginate(res)

@router.get('/get_data/id')
async def get_item_(session: AsyncSession = Depends(get_async_session),
                    id: int = Query()):
    res = await get_item(session, id)
    return res

@router.get('/get_data/countrus')
async def get_countru_(session: AsyncSession = Depends(get_async_session)):
    res = await get_countru(session)
    return res



@router.get('/get_data/countru')
async def get_item_countru(session: AsyncSession = Depends(get_async_session),
                    countru: str = Query(),
                    page: int = Query(ge=0, default=0), 
                    size: int = Query(ge=1, default=25)) -> Page[shemas.RawData]:
    res = await get_items_countru(session, countru)
    return paginate(res)

@router.get('/get_data/category')
async def get_category_(session: AsyncSession = Depends(get_async_session)):
    res = await get_category(session)
    return res

@router.get('/get_data/category_')
async def get_items_category_(session: AsyncSession = Depends(get_async_session),
                    category: str = Query(),
                    page: int = Query(ge=0, default=0), 
                    size: int = Query(ge=1, default=25)) -> Page[shemas.RawData]:
    
    res = await get_items_category(session,category)
    return paginate(res)


@router.get('/get_data/sites')
async def get_data_site(session: AsyncSession = Depends(get_async_session)):
    
    res = await get_net_href(session)
    return res

@router.get('/get_data/sites_')
async def get_items_sites_(session: AsyncSession = Depends(get_async_session),
                    sites: str = Query(),
                    page: int = Query(ge=0, default=0), 
                    size: int = Query(ge=1, default=25)) -> Page[shemas.RawData]:
    
    res = await get_items_net_href_(session,sites)
    return paginate(res)